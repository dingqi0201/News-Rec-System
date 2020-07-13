# -*- coding:utf-8 -*-
"""
    bgp.py
    ~~~~~~~~
    BGP 管理

    :author: Fufu, 2019/9/21
"""
from sqlalchemy import desc

from ..models.bgp import TBBGP
from ..libs.exceptions import APIFailure


class BGPCharge:
    """BGP 相关数据表操作"""

    @staticmethod
    def add(data, as_api=False):
        """
        新增 BGP

        :param data: dict
        :param as_api: True 入库失败返回 APIException
        :return:
        """
        res = TBBGP().insert(data)
        if not res and as_api:
            raise APIFailure('BGP 入库失败')

        return res

    @staticmethod
    def get_list(where=None, pages=None, order_by=None):
        """
        获取 BGP 列表(分页)

        :param where: dict
        :param pages: dict, 分页参数 e.g. {'page': 1, 'limit': 60, 'count': 0}
        :param order_by: dict, 排序字段 e.g. {'bgp_update'} {'bgp_update': 'desc'}
        :return: list
        """
        where = dict(filter(lambda x: tuple(x)[1], where.items())) if where else {}
        q = TBBGP.query.filter_by(**where)

        if order_by and isinstance(order_by, dict):
            for field, order_type in order_by.items():
                q = q.order_by(desc(field) if order_type == 'desc' else field)
        else:
            # 默认 BGP 最后更新时间升序
            q = q.order_by('bgp_update')

        count = 0
        if pages and isinstance(pages, dict):
            page = pages.get('page', 1)
            limit = pages.get('limit', 60)
            count = pages.get('count', 0)
            # 为了演示分页, 强制每页显示数量为 1
            limit = 1
            # 第一次请求由数据库计算总数(每次都由数据库计算也行, 实时性更好), 后续由前端返回总数, 减少数据库请求
            if not count:
                count = q.count()
            q = q.limit(limit).offset((page - 1) * limit)

        # bgp_test_decimal 字段将不会发送给前端. 比如根据权限不同, 敏感字段可选是否发送给前端显示
        return q.hide_keys_dicts(['bgp_test_decimal']), count
