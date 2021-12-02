#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2021/9/24 14:08 
@Author : harvey
@File : db_connection.py 
@Software: PyCharm
@Desc: 
@Module
"""

from multiprocessing import Lock
import os
import logging

import pymysql

from django.db import connection

from assets.models.assets import AssetsDbInstance

logger = logging.getLogger(__name__)


def raw_sql(sql):
    with connection.cursor() as cursor:
        cursor.execute(f"{sql}")
        row = cursor.fetchall()
    return row


# lock = Lock()


class ConMySQL():
    def __init__(self, host='127.0.0.1', port=3306, user='root', passwd='', db=''):
        try:
            self.con = pymysql.connect(host=host, user=user, passwd=passwd, port=port, db=db, charset='utf8mb4')
        except Exception as e:
            msg = f"\033[31;1mError:Can't connect {host}:{port},{e.args[1]} \033[0m"
            print(msg)
            # os._exit(1)
        self.cursor = self.con.cursor()

    def query_string(self, sql):
        # lock.acquire()
        self.cursor.execute(sql)
        # lock.release()
        # self.con.close()
        return self.cursor.fetchall()[0][0]

    # 返回值为2元tuple
    def query_tuple(self, sql):
        # lock.acquire()
        self.cursor.execute(sql)
        # lock.release()
        self.con.close()
        return self.cursor.fetchall()

    # 返回值为2元tuple中的第一个元素，仍为tuple
    def query_tuple_first(self, sql):
        # lock.acquire()
        self.cursor.execute(sql)
        # lock.release()
        self.con.close()
        return self.cursor.fetchall()[0]

    def insert(self, sql):
        # lock.acquire()
        self.cursor.execute(sql)
        # lock.release()
        # self.con.close()
        return {'header': self.cursor.description, 'result': self.cursor.fetchall()}


def get_goInception_client():
    ins = AssetsDbInstance.objects.filter(type='goInception').first()
    host = ins.db_host
    port = ins.db_port
    user = ins.root_user
    pwd = ins.decrypt_password()
    goInceptionClient = ConMySQL(host=host, port=port, user=user, passwd=pwd)
    return goInceptionClient


class goInception():
    @classmethod
    def execute(cls, db_user_instance, sql, execute=0, check=1):
        db_ins = AssetsDbInstance.objects.get(pk=db_user_instance.ins_id.hex)
        host = db_ins.db_host
        port = db_ins.db_port
        db_name = db_user_instance.db_name
        user = db_user_instance.db_user
        pwd = db_user_instance.decrypt_password()
        client = get_goInception_client()
        """goInception param https://hanchuanchuan.github.io/goInception/zh/params.html"""
        proxy_sql = f'''/*--user={user};--password='{pwd}';--host={host};--execute={execute};--check={check};--port={port};*/
            inception_magic_start; 
            use {db_name};
            {sql}           
            inception_magic_commit;'''
        logger.debug(f"proxy sql is ==={proxy_sql}")
        logger.debug(client.cursor.description)
        return client.insert(proxy_sql)


def get_tidb_client(instance):
    host = instance.db_host
    port = instance.db_port
    user = instance.root_user
    pwd = instance.decrypt_password()
    return ConMySQL(host=host, port=port, user=user, passwd=pwd)
