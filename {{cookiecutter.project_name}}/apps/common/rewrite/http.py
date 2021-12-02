#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2021/9/15 20:04 
@Author : harvey
@File : http.py 
@Software: PyCharm
@Desc: 重写drf的resonpse
@Module
"""

from rest_framework.response import Response
from rest_framework.serializers import Serializer

from common.params import code

__all__ = ['SuccessResponse', ]


class BaseResponse(Response):
    def __init__(self, data=None, status=200,
                 template_name=None, headers=None,
                 exception=False, content_type=None,
                 code=None, message=None):

        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super().__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        # self.data = data
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type
        self.code = code
        self.message = message
        self.data = {"code": self.code, "message": self.message, "data": data}

        if headers:
            for name, value in headers.items():
                self[name] = value


class SuccessResponse(BaseResponse):
    def __init__(self, data=None, status=200,
                 template_name=None, headers=None,
                 exception=False, content_type=None,
                 code=code.OK_CODE, message=code.OK_MSG,
                 sub_code=''):

        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super().__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        # self.data = data
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type
        self.code = code
        self.message = message
        self.sub_code = sub_code
        self.status = status
        self.data = {"code": self.code, "message": self.message, "data": data, "sub_code":self.status}

        if headers:
            for name, value in headers.items():
                self[name] = value
