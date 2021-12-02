#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2021/10/7 00:11 
@Author : harvey
@File : encode.py 
@Software: PyCharm
@Desc: 
@Module
"""

from itsdangerous import (
    TimedJSONWebSignatureSerializer, JSONWebSignatureSerializer,
    BadSignature, SignatureExpired
)

from django.conf import settings


class Singleton(type):
    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance
        else:
            return cls.__instance


class Signer(metaclass=Singleton):
    """用来加密,解密,和基于时间戳的方式验证token"""

    def __init__(self, secret_key=None):
        self.secret_key = secret_key

    def sign(self, value):
        s = JSONWebSignatureSerializer(self.secret_key, algorithm_name='HS256')
        return s.dumps(value).decode()

    def unsign(self, value):
        if value is None:
            return value
        s = JSONWebSignatureSerializer(self.secret_key, algorithm_name='HS256')
        try:
            return s.loads(value)
        except BadSignature:
            return None

    def sign_t(self, value, expires_in=3600):
        s = TimedJSONWebSignatureSerializer(self.secret_key, expires_in=expires_in)
        return str(s.dumps(value), encoding="utf8")

    def unsign_t(self, value):
        s = TimedJSONWebSignatureSerializer(self.secret_key)
        try:
            return s.loads(value)
        except (BadSignature, SignatureExpired):
            return None


def get_signer():
    s = Signer(settings.SECRET_KEY)
    return s


signer = get_signer()
