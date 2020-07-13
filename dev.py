#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    dev.py
    ~~~~~~~~
    启动服务(使用 development 配置)：python3 dev.py

    :author: Fufu, 2019/9/2
"""
from app import create_app

app = create_app(config_name='development')

if __name__ == '__main__':
    app.run()
