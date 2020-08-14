#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    gunicorn.conf.py
    ~~~~~~~~
    gunicorn 示例配置, 仅 Linux 使用:
    pip3 install gunicorn gevent
    gunicorn -b :5200 start:app
    gunicorn -c ./scripts/gunicorn/gunicorn.conf.py start:app

    https://docs.gunicorn.org/en/stable/settings.html
    https://docs.gunicorn.org/en/stable/deploy.html

    :author: Fufu, 2020/8/14
"""
import gevent.monkey

gevent.monkey.patch_all()

import multiprocessing
import os

if not os.path.exists('logs'):
    os.mkdir('logs')

# debug, info, warning, error, critical
loglevel = 'debug'
debug = True

# nginx 代理一般启环回地址或socket
# bind = '127.0.0.1:5200'
# bind = 'unix:/run/pyadmin.sock'

# 直接对外提供服务
bind = ':5200'

pidfile = 'logs/gunicorn.pid'
logfile = 'logs/debug.log'
errorlog = 'logs/error.log'
accesslog = 'logs/access.log'

# 启动的进程数, 项目中用了 flask_apscheduler 需要解决重复执行问题(锁或这里 workers = 1)
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
# worker_class = 'gunicorn.workers.ggevent.GeventWorker'
# threads = 2

daemon = True

x_forwarded_for_header = 'X-FORWARDED-FOR'
