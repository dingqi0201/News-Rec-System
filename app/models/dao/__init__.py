#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    __init__.py
    ~~~~~~~~

    :author: Fufu, 2020/12/18
"""
from abc import abstractmethod, ABC
from datetime import datetime, date

from flask import current_app
from sqlalchemy import text

from ...libs.helper import list2dict


class BaseDao(ABC):
    """数据库操作基类"""

    conn = {}

    @classmethod
    @abstractmethod
    def get_conn(cls, tag):
        """数据库连接"""
        pass

    @classmethod
    def execute(cls, sql, tag=''):
        try:
            db = cls.get_conn(tag)
            with db.begin():
                return db.execute(text(sql)).fetchall()
        except Exception as e:
            current_app.logger.error('db_charge execute err: {0!r}'.format(e))

    @classmethod
    def result_tpl(cls, subject, params=None, schema=None):
        """
        根据数据请求模板请求数据

        :param subject: str, 查询主题
        :param params: dict, 参数值, 用于替换查询语句对应变量
        :param schema: list, 表头
        :return:
        """
        query_tpl = current_app.config['QUERY_TPL'].get(subject)
        if not query_tpl or not isinstance(query_tpl, (tuple, list)) or len(query_tpl) < 2 or not query_tpl[0]:
            return None

        # 查询参数
        tag = query_tpl[0]
        sql = str(query_tpl[1])
        if isinstance(params, dict):
            for k, v in params.items():
                if isinstance(v, datetime):
                    v = v.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(v, date):
                    v = v.strftime('%Y-%m-%d')
                sql = sql.replace('[[.' + k + '.]]', v if isinstance(v, str) else str(v))

        if current_app.debug:
            current_app.logger.debug('\n{}\n{}'.format(tag, sql))

        data = cls.execute(sql, tag)

        # 整合表头, 转为字典, 否则返回列表.元祖
        return list2dict(schema, data) if schema else data
