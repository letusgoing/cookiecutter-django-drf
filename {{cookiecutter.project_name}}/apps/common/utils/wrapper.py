#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2021/10/8 10:12 
@Author : harvey
@File : wrapper.py 
@Software: PyCharm
@Desc: 
@Module
"""

import logging
import time

logger = logging.getLogger(__name__)


def timeit(func):
    def wrapper(*args, **kwargs):
        name = func
        for attr in ('__qualname__', '__name__'):
            if hasattr(func, attr):
                name = getattr(func, attr)
                break

        logger.debug("Start call: {}".format(name))
        now = time.time()
        result = func(*args, **kwargs)
        using = (time.time() - now) * 1000
        msg = "End call {}, using: {:.1f}ms".format(name, using)
        logger.debug(msg)
        return result

    return wrapper
