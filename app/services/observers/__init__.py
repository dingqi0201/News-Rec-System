# -*- coding:utf-8 -*-
"""
    observer.py
    ~~~~~~~~
    信号, 事件增加订阅

    2020/12/20
"""
from .async_with_app_demo import async_width_app_handler
from .observer import Observer
from .sys_admin import sys_admin_handler
from .user_logined import user_logined_handler
from ..events import event_user_logined, event_sys_admin, event_async_with_app_demo

observer = Observer()
observer.add(event_user_logined, user_logined_handler)
observer.add(event_sys_admin, sys_admin_handler)
observer.add(event_async_with_app_demo, async_width_app_handler)
