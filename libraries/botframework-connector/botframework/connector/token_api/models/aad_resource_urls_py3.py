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


class AadResourceUrls(Model):
    """AadResourceUrls.

    :param resource_urls:
    :type resource_urls: list[str]
    """

    _attribute_map = {
        'resource_urls': {'key': 'resourceUrls', 'type': '[str]'},
    }

    def __init__(self, *, resource_urls=None, **kwargs) -> None:
        super(AadResourceUrls, self).__init__(**kwargs)
        self.resource_urls = resource_urls
