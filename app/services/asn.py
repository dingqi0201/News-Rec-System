# -*- coding:utf-8 -*-
"""
    asn.py
    ~~~~~~~~
    ASN 相关服务

    2020/9/18
"""
from flask import current_app

from .log import LogCharge
from ..libs.exceptions import APIFailure
from ..models.bgp import *


class ASNCharge:
    """ASN 相关数据表操作"""

    @staticmethod
    def add(data, as_api=False):
        """
        新增 ASN

        :param data: dict
        :param as_api: True 入库失败返回 APIException
        :return:
        """
        res = TBASN().insert(data)

        # 1. 可选写文件日志
        current_app.logger.info('{}, {}'.format(res, data))

        # 2. 可选写数据库日志
        LogCharge.to_db({'log_content': data})

        # 3. 可选使用信号机制, 见: UserCharge.authorize()
        # event_asn_changed.send(**data)

        if not res and as_api:
            raise APIFailure('ASN 入库失败')

        # 更新 ASN_LIST 缓存数据
        current_app.config['ASN_LIST'].add(data['asn'])

        return res

    @staticmethod
    def get_list(asn=None):
        """
        获取 ASN 列表(暂未分页)

        e.g.::

            ASNCharge.get_list(31001)
            ASNCharge.get_list()

        :return: list
        """
        if asn:
            return TBASN.query.filter_by(asn=asn).to_dicts

        return TBASN.query.to_dicts
