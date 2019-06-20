# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import re
from datetime import datetime, timedelta
from typing import Union, Awaitable, Callable

from botbuilder.core import CardFactory, MessageFactory, InvokeResponse, TurnContext
from botbuilder.dialogs import Dialog, DialogContext, DialogTurnResult
from botbuilder.schema import Activity, ActivityTypes, ActionTypes, CardAction, InputHints, SigninCard, OAuthCard, TokenResponse
from botframework.connector import Channels
from .prompt_options import PromptOptions
from .oauth_prompt_settings import OAuthPromptSettings
from .prompt_validator_context import PromptValidatorContext
from .prompt_recognizer_result import PromptRecognizerResult

class OAuthPrompt(Dialog):
    """
    Creates a new prompt that asks the user to sign in using the Bot Framework Single Sign On (SSO) service.
    The prompt will attempt to retrieve the users current token and if the user isn't signed in, it
    will send them an `OAuthCard` containing a button they can press to sign in. Depending on the channel,
    the user will be sent through one of two possible sign-in flows:
    - The automatic sign-in flow where once the user signs in, the SSO service will forward
    the bot the users access token using either an `event` or `invoke` activity.
    - The "magic code" flow where once the user signs in, they will be prompted by the SSO service
    to send the bot a six digit code confirming their identity. This code will be sent as a 
    standard `message` activity.
    Both flows are automatically supported by the `OAuthPrompt` and they only thing you need to be careful of
    is that you don't block the `event` and `invoke` activities that the prompt might be waiting on.
    Note:
    You should avaoid persisting the access token with your bots other state. The Bot Frameworks SSO service
    will securely store the token on your behalf. If you store it in your bots state,
    it could expire or be revoked in between turns.
    When calling the prompt from within a waterfall step, you should use the token within the step
    following the prompt and then let the token go out of scope at the end of your function
    Prompt Usage
    When used with your bots `DialogSet`, you can simply add a new instance of the prompt as a named dialog using `DialogSet.add()`.
    You can then start the prompt from a waterfall step using either `DialogContext.begin()` or `DialogContext.prompt()`.
    The user will be prompted to sign in as needed and their access token will be passed as an argument to the callers next waterfall step.
    """

    def __init__(self, dialog_id: str, settings: OAuthPromptSettings, validator: Callable[[PromptValidatorContext], Awaitable[bool]]=None):
        super().__init__(dialog_id)
        self._validator = validator

        if not settings:
            raise TypeError('OAuthPrompt requires OAuthPromptSettings.')

        self._settings = settings
        self._validator = validator
    
    async def begin_dialog(self, dialog_context: DialogContext, options: PromptOptions= None) -> DialogTurnResult:
        if dialog_context is None:
            raise TypeError(f'Expected DialogContext but got NoneType instead')
        
        if options is None:
            raise TypeError(f'Expected PromptOptions but got NoneType instead')
        
        #Ensure prompts have input hint set
        if options.prompt and not options.prompt.input_hint:
            options.prompt.input_hint = InputHints.expecting_input
        
        if options.retry_prompt and not options.retry_prompt.input_hint:
            options.prompt.input_hint = InputHints.expecting_input
        
        #Initialize prompt state
        timeout = self._settings.timeout if isinstance(self._settings.timeout, int) else 900000
        state = dialog_context.active_dialog.state
        state['state'] = {}
        state['options'] = options
        state['expires'] = datetime.now() + timedelta(seconds=timeout/1000)

        output = await self.get_user_token(dialog_context.context)
        
        if output is not None:
            return await dialog_context.end_dialog(output)
        else:
            await self.send_oauth_card(dialog_context.context, options.prompt)
            return Dialog.end_of_turn
    
    async def continue_dialog(self, dialog_context: DialogContext) -> DialogTurnResult:
        # Recognize token
        recognized = await self._recognize_token(dialog_context.context)

        # Check for timeout
        state = dialog_context.active_dialog.state
        is_message = dialog_context.activity.type == ActivityTypes.message
        has_timed_out = is_message and (datetime.now() > state['expires'])

        if has_timed_out:
            return await dialog_context.end_dialog(None)
        else:
            if state['state'].get('attemptCount') is None:
                state['state']['attemptCount'] = 1
            
            # Validate the return value
            is_valid = False
            if self._validator is not None:
                is_valid = await self._validator(PromptValidatorContext(
                    dialog_context.context,
                    recognized,
                    state['state'],
                    state['options'],
                    state['state']['attemptCount']
                ))
            elif recognized.succeded:
                is_valid = True
            
            # Return recognized value or re-prompt
            if is_valid:
                return await dialog_context.end_dialog(recognized.value)
            else:
                # Send retry prompt
                if not dialog_context.context.responded and is_message and state['options'].retry_prompt is not None:
                    await dialog_context.context.send_activity(state['options'].retry_prompt)
                
                return Dialog.end_of_turn

    async def get_user_token(self, context: TurnContext, code: str= None) -> TokenResponse:
        adapter = context.adapter

        # Validate adapter type
        if not hasattr(adapter, 'get_user_token'):
            raise Exception('OAuthPrompt.get_user_token(): not supported for the current adapter.')

        return await adapter.get_user_token(context, self._settings.connection_name, code)

    async def sign_out_user(self, context: TurnContext):
        adapter = context.adapter

        # Validate adapter type
        if not hasattr(adapter, 'sign_out_user'):
            raise Exception('OAuthPrompt.sign_out_user(): not supported for the current adapter.')

        return await adapter.sign_out_user(context, self._settings.connection_name)

    async def send_oauth_card(self, context: TurnContext, prompt: Union[Activity, str]= None):
        if not isinstance(prompt, Activity):
            prompt = MessageFactory.text(prompt or '', None, InputHints.expecting_input)
        else:
            prompt.input_hint = prompt.input_hint or InputHints.expecting_input
        
        prompt.attachments = prompt.attachments or []

        if self._channel_suppports_oauth_card(context.activity.channel_id):
            if any(att.content_type == CardFactory.content_types.oauth_card for att in prompt.attachments):
                prompt.attachments.append(CardFactory.oauth_card(OAuthCard(
                    text= self._settings.text,
                    connection_name= self._settings._connection_name,
                    buttons= [
                        CardAction(
                            title= self._settings.title,
                            text= self._settings.text,
                            type= ActionTypes.signin
                        )
                    ]
                )))
        else:
            if any(att.content_type == CardFactory.content_types.signin_card for att in prompt.attachments):
                if not hasattr(context.adapter, 'get_oauth_sign_in_link'):
                    raise Exception('get_oauth_sign_in_link(): not supported by the current adapter')

                link = await context.adapter.get_oauth_sign_in_link(context, self._settings.connection_name)
                prompt.attachments.append(CardFactory.signin_card(SigninCard(
                    text= self._settings.text,
                    buttons= [
                        CardAction(
                            title= self._settings.title,
                            value= link,
                            type= ActionTypes.signin
                        )
                    ]
                )))
        
        # Send prompt
        await context.send_activity(prompt)
    
    async def _recognize_token(self, context: TurnContext) -> PromptRecognizerResult:
        if self._is_token_response_event(context):
            token = context.activity.value
        elif self._is_teams_verification_invoke(context):
            code = context.activity.value.state
            try:
                token = await self.get_user_token(context, code)
                if token is not None:
                    await context.send_activity(Activity(type='invokeResponse', value=InvokeResponse(200)))
                else:
                    await context.send_activity(Activity(type='invokeResponse', value=InvokeResponse(404)))
            except Exception:
                context.send_activity(Activity(type='invokeResponse', value=InvokeResponse(500)))
        elif context.activity.type == ActivityTypes.message:
            match = re.match(r'(?<!\d)\d{6}(?!\d)', context.activity.text)
            if match:
                token = await self.get_user_token(context, match[0])
        
        return PromptRecognizerResult(True, token) if token is not None else PromptRecognizerResult()
    
    def _is_token_response_event(self, context: TurnContext) -> bool:
        activity = context.activity

        return activity.type == ActivityTypes.event and activity.name == 'tokens/response'
    
    def _is_teams_verification_invoke(self, context: TurnContext) -> bool:
        activity = context.activity

        return activity.type == ActivityTypes.invoke and activity.name == 'signin/verifyState'
    
    def _channel_suppports_oauth_card(self, channel_id: str) -> bool:
        if channel_id in [
            Channels.ms_teams,
            Channels.cortana,
            Channels.skype,
            Channels.skype_for_business
        ]:
            return False
        
        return True