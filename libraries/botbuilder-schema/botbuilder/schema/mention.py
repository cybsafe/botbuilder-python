# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class Mention(Model):
    """Mention information (entity type: "mention").

    :param mentioned: The mentioned user
    :type mentioned: ~botframework.connector.models.ChannelAccount
    :param text: Sub Text which represents the mention (can be null or empty)
    :type text: str
    :param type: Type of this entity (RFC 3987 IRI)
    :type type: str
    """

    _attribute_map = {
        'mentioned': {'key': 'mentioned', 'type': 'ChannelAccount'},
        'text': {'key': 'text', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(Mention, self).__init__(**kwargs)
        self.mentioned = kwargs.get('mentioned', None)
        self.text = kwargs.get('text', None)
        self.type = kwargs.get('type', None)
