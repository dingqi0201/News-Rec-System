#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    async_with_app_demo.py
    ~~~~~~~~

    :author: Fufu, 2020/7/10
"""
import time

from ...libs.helper import async_task, debug
from ...models.user import TBUser


@async_task
def async_width_app_handler(sender, **data):
    time.sleep(5)

    debug(dir(sender))

    with sender.app_context():
        res = TBUser.query.to_dicts
        debug(res)

    debug(data)
