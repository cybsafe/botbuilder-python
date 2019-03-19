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

try:
    from .token_response_py3 import TokenResponse
    from .inner_http_error_py3 import InnerHttpError
    from .error_py3 import Error
    from .error_response_py3 import ErrorResponse, ErrorResponseException
    from .aad_resource_urls_py3 import AadResourceUrls
    from .token_status_py3 import TokenStatus
except (SyntaxError, ImportError):
    from .token_response import TokenResponse
    from .inner_http_error import InnerHttpError
    from .error import Error
    from .error_response import ErrorResponse, ErrorResponseException
    from .aad_resource_urls import AadResourceUrls
    from .token_status import TokenStatus

__all__ = [
    'TokenResponse',
    'InnerHttpError',
    'Error',
    'ErrorResponse', 'ErrorResponseException',
    'AadResourceUrls',
    'TokenStatus',
]
