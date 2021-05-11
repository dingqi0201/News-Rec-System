# -*- coding:utf-8 -*-
"""
    events.py
    ~~~~~~~~
    自定义信号, 事件

    2020/12/20
"""
from blinker import signal

# 用户登录成功
event_user_logined = signal('event_user_logined')

# 系统管理操作(用户授权/权限组管理等)
event_sys_admin = signal('event_sys_admin')

# app 上下文环境示例
event_async_with_app_demo = signal('event_async_with_app_demo')
