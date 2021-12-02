#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2021/10/7 15:40 
@Author : harvey
@File : basic.py 
@Software: PyCharm
@Desc: 
@Module
"""

from rest_framework import permissions


class IsValidUser(permissions.IsAuthenticated, permissions.BasePermission):
    """Allows access to valid user, is active and not expired"""

    def has_permission(self, request, view):
        return super(IsValidUser, self).has_permission(request, view) \
               and request.user.is_valid


class IsSuperUser(IsValidUser):
    def has_permission(self, request, view):
        return super(IsSuperUser, self).has_permission(request, view) \
               and request.user.is_superuser
