#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2021/9/15 20:56 
@Author : harvey
@File : middleware.py 
@Software: PyCharm
@Desc: 
@Module
"""

from django.utils.deprecation import MiddlewareMixin

from .middleware_handler import response_handler



class GlobalExceptionMiddleware(MiddlewareMixin):
    """改写reponse，增加自定义状态，修改http status_code"""
    def process_response(self, request, response):
        response = response_handler(response)
        # print("10"*100)
        return response


    def process_exception(self, request, exception):
        # print(exception)
        print(exception.__dict__)
        raise exception