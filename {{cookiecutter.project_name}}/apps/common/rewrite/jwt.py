#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2021/9/15 20:10 
@Author : harvey
@File : jwt.py 
@Software: PyCharm
@Desc: 重写drf_jwt ObtainJSONWebToken视图的返回信息
@Module
"""
import datetime

from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.views import jwt_response_payload_handler
from rest_framework.settings import api_settings
from rest_framework import status

from common.rewrite.http import Response


class Userlogin(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
