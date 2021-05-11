# -*- coding:utf-8 -*-
"""
    log.py
    ~~~~~~~~
    日志相关服务

    2020/9/16
"""
from flask import request, json
from flask_login import current_user
from sqlalchemy import desc

from ..libs.exceptions import APIFailure
from ..models.user import TBLog


class LogCharge:
    """日志数据表相关操作"""

    @staticmethod
    def to_db(data=None, as_api=False):
        """
        记录日志到数据库

        :param data: dict, 键必须是 log 表字段名
        :param as_api:
        :return:
        """
        log = {
            'log_action': request.endpoint,
            'log_operator': getattr(current_user, 'realname', request.remote_addr)
        }

        isinstance(data, dict) and log.update(data)
        if not isinstance(log.get('log_content', ''), str):
            log['log_content'] = json.dumps(log['log_content'], ensure_ascii=False)

        res = TBLog().insert(log)
        if not res and as_api:
            raise APIFailure('日志入库失败')

        return res

    @staticmethod
    def get_list(where=None, limit=200):
        """
        获取日志列表(暂未分页)

        :param where: dict
        :param limit: int
        :return: list
        """
        where = dict(filter(lambda x: tuple(x)[1] not in [None, ''], where.items())) if where else {}
        return TBLog.query.filter_by(**where).order_by(desc('log_id')).limit(limit).to_dicts
