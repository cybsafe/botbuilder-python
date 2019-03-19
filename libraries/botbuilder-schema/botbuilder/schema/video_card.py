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


class VideoCard(Model):
    """Video card.

    :param title: Title of this card
    :type title: str
    :param subtitle: Subtitle of this card
    :type subtitle: str
    :param text: Text of this card
    :type text: str
    :param image: Thumbnail placeholder
    :type image: ~botframework.connector.models.ThumbnailUrl
    :param media: Media URLs for this card. When this field contains more than
     one URL, each URL is an alternative format of the same content.
    :type media: list[~botframework.connector.models.MediaUrl]
    :param buttons: Actions on this card
    :type buttons: list[~botframework.connector.models.CardAction]
    :param shareable: This content may be shared with others (default:true)
    :type shareable: bool
    :param autoloop: Should the client loop playback at end of content
     (default:true)
    :type autoloop: bool
    :param autostart: Should the client automatically start playback of media
     in this card (default:true)
    :type autostart: bool
    :param aspect: Aspect ratio of thumbnail/media placeholder. Allowed values
     are "16:9" and "4:3"
    :type aspect: str
    :param duration: Describes the length of the media content without
     requiring a receiver to open the content. Formatted as an ISO 8601
     Duration field.
    :type duration: str
    :param value: Supplementary parameter for this card
    :type value: object
    """

    _attribute_map = {
        'title': {'key': 'title', 'type': 'str'},
        'subtitle': {'key': 'subtitle', 'type': 'str'},
        'text': {'key': 'text', 'type': 'str'},
        'image': {'key': 'image', 'type': 'ThumbnailUrl'},
        'media': {'key': 'media', 'type': '[MediaUrl]'},
        'buttons': {'key': 'buttons', 'type': '[CardAction]'},
        'shareable': {'key': 'shareable', 'type': 'bool'},
        'autoloop': {'key': 'autoloop', 'type': 'bool'},
        'autostart': {'key': 'autostart', 'type': 'bool'},
        'aspect': {'key': 'aspect', 'type': 'str'},
        'duration': {'key': 'duration', 'type': 'str'},
        'value': {'key': 'value', 'type': 'object'},
    }

    def __init__(self, **kwargs):
        super(VideoCard, self).__init__(**kwargs)
        self.title = kwargs.get('title', None)
        self.subtitle = kwargs.get('subtitle', None)
        self.text = kwargs.get('text', None)
        self.image = kwargs.get('image', None)
        self.media = kwargs.get('media', None)
        self.buttons = kwargs.get('buttons', None)
        self.shareable = kwargs.get('shareable', None)
        self.autoloop = kwargs.get('autoloop', None)
        self.autostart = kwargs.get('autostart', None)
        self.aspect = kwargs.get('aspect', None)
        self.duration = kwargs.get('duration', None)
        self.value = kwargs.get('value', None)
