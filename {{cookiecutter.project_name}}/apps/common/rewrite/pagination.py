#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2021/10/11 01:57 
@Author : harvey
@File : pagination.py 
@Software: PyCharm
@Desc: 
@Module
"""

from collections import OrderedDict

from common.rewrite.http import SuccessResponse as Response


from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """改写Response结构"""
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
        ]))