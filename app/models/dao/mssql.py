# -*- coding:utf-8 -*-
"""
    mssql.py
    ~~~~~~~~
    SQLServer 数据库操作
    Ref: https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server

    :author: Fufu, 2020/12/17
"""
from flask import current_app
from sqlalchemy import create_engine

from . import BaseDao


class MSSQL(BaseDao):
    """SQLServer 数据库操作"""

    tag = 'MSSQL_DATABASE_URI'

    @classmethod
    def get_conn(cls, tag=''):
        tag = tag.strip().upper() if tag else cls.tag
        if cls.conn.get(tag):
            return cls.conn[tag]

        try:
            cls.conn[tag] = create_engine(current_app.config.get(tag), max_identifier_length=128).connect()
            return cls.conn[tag]
        except Exception as e:
            current_app.logger.error('mssql_charge err: {0} {1!r}'.format(tag, e))
