# -*- coding:utf-8 -*-
"""
    sys_admin.py
    ~~~~~~~~
    处理系统配置事件

    :author: Fufu, 2019/12/20
"""
from ..log import LogCharge


def sys_admin_handler(sender, **data):
    """
    系统配置事件回调

    e.g.::

        event_sys_admin.send(log_status=1, log_content={'fufu': 1})

    :param sender: 信号发送者/事件触发者
    :param data: 由发送者传递
    :return:
    """
    # 日志
    LogCharge.to_db({
        'log_status': 1 if data.pop('log_status', 0) else 0,
        'log_content': data.pop('log_content', ''),
    })
