#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    start.py
    ~~~~~~~~
    启动服务(使用环境变量中的配置文件)：python3 start.py

    2020/9/2
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
