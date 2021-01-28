# -*- coding:utf-8 -*-
"""
    mysql.py
    ~~~~~~~~
    MySQL 数据库操作

    :author: Fufu, 2020/12/17
"""
from flask import current_app
from sqlalchemy import create_engine

from . import BaseDao


class MYSQL(BaseDao):
    """MySQL 数据库操作"""

    tag = 'MYSQL_DATABASE_URI'

    @classmethod
    def get_conn(cls, tag=''):
        tag = tag.strip().upper() if tag else cls.tag
        if cls.conn.get(tag):
            return cls.conn[tag]

        try:
            cls.conn[tag] = create_engine(current_app.config.get(tag), max_identifier_length=128).connect()
            return cls.conn[tag]
        except Exception as e:
            current_app.logger.error('mysql_charge err: {0} {1!r}'.format(tag, e))
