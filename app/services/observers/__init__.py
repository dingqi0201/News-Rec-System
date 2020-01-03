# -*- coding:utf-8 -*-
"""
    observer.py
    ~~~~~~~~
    信号, 事件增加订阅

    :author: Fufu, 2019/12/20
"""
from .observer import Observer
from .sys_admin import sys_admin_handler
from .user_logined import user_logined_handler
from ..events import event_user_logined, event_sys_admin

observer = Observer()
observer.add(event_user_logined, user_logined_handler)
observer.add(event_sys_admin, sys_admin_handler)
