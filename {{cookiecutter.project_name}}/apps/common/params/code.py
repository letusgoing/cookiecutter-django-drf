#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2021/9/15 20:06 
@Author : harvey
@File : code.py 
@Software: PyCharm
@Desc: 定义全局响应状态码（非http状态）
@Module
"""

OK_CODE = 0
OK_MSG = 'OK'
"""参数校验异常类"""
PARAM_ERROR_CODE = 10001
PARAM_ERROR_MSG = '参数校验异常'

"""登录及权限类类"""
LOGIN_ERROR_CODE = 40001
LOGIN_ERROR_MSG = "用户名或密码错误"
EXPIRE_ERROR_CODE = 40002
EXPIRE_ERROR_MSG = "token已失效，请重新登陆"
PERMISSON_ERROR_CODE = 40003
PERMISSION_ERROR_CODE = "未授权的操作"

"""服务端异常类"""


"""未知错误及状态码"""
OTHER_ERROR_CODE = 60001
OTHER_ERROR_MSG = "服务端异常"
