# -*- coding:utf-8 -*-
"""
    dbcache.py
    ~~~~~~~~
    数据表缓存

    :author: Fufu, 2020/9/18
"""
from .bgp import TBASN


def init_db_cache(app):
    """
    初始化数据库缓存

    :param app:
    :return:
    """
    # 初始化 ASN 列表, 从 MySQL 加载到内存, 使用时不再查库
    data = TBASN.query.all()
    app.config['ASN_LIST'] = {x.asn for x in data}
