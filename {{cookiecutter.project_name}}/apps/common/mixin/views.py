#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2021/9/22 22:32 
@Author : harvey
@File : views.py 
@Software: PyCharm
@Desc: 
@Module
"""

from common.auth.jwt import CustomJwtAuthentication


class AuthenticationMixin:
    authentication_classes = [CustomJwtAuthentication]
