#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2021/9/19 21:41 
@Author : harvey
@File : middleware_handler.py
@Software: PyCharm
@Desc: 
@Module
"""

import logging

from common.params import code as custom_code


logger = logging.getLogger(__name__)

def response_handler(response):
    """改写reponse，增加自定义状态，修改http status_code"""
    """主要是针对django authentication permisson校验异常类"""

    # print('100'*100)
    # print(response.__dict__)

    is_logger = False
    if not hasattr(response, 'data'):
        return response
    data = response.data
    """已存在自定义状态码，则直接返回"""
    if data.get('code') is not None:
        return response
    status_code = int(response.status_code)
    if status_code == 200:
        code = custom_code.OK_CODE
        message = custom_code.OK_MSG
    elif status_code == 401:
        code = custom_code.EXPIRE_ERROR_CODE
        message = custom_code.EXPIRE_ERROR_MSG
    else:
        is_logger = True
        code = custom_code.OTHER_ERROR_CODE
        message = custom_code.OTHER_ERROR_MSG
    response_data = {
        'code': code,
        'message': message,
        'data': response.data
    }
    if is_logger:
        logger.error(f"{response_data}")
    response.data = response_data
    response.status_code = 200
    response._is_rendered = False
    return response.render()
