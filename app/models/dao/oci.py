# -*- coding:utf-8 -*-
"""
    oci.py
    ~~~~~~~~
    Oracle 数据库操作
    Ref: https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html

    :author: Fufu, 2020/12/17
"""
import cx_Oracle
from flask import current_app
from sqlalchemy import create_engine

from . import BaseDao


class OCI(BaseDao):
    """Oracle 数据库操作"""

    tag = 'OCI_DATABASE_URI'

    @classmethod
    def get_conn(cls, tag=''):
        tag = tag.strip().upper() if tag else cls.tag
        if cls.conn.get(tag):
            return cls.conn[tag]

        try:
            cx_Oracle.init_oracle_client(lib_dir=current_app.config.get('OCI_LIB_PATH'))
        except Exception:
            pass

        try:
            cls.conn[tag] = create_engine(
                current_app.config.get(tag),
                connect_args={
                    'encoding': 'UTF-8',
                    'nencoding': 'UTF-8',
                    'events': True
                },
                max_identifier_length=128,
            ).connect()
            return cls.conn[tag]
        except Exception as e:
            current_app.logger.error('oci_charge err: {0} {1!r}'.format(tag, e))
