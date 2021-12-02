#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2021/9/19 19:31 
@Author : harvey
@File : custom_handler.py
@Software: PyCharm
@Desc: 
@Module
"""

import logging

logger = logging.getLogger(__name__)

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    print(exc)
    print("custom ")
    logger.warning(response.__dict__)


    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response
