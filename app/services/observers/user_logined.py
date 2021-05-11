# -*- coding:utf-8 -*-
"""
    user_logined.py
    ~~~~~~~~
    处理用户登录成功事件

    2020/12/20
"""
from flask import current_app, request
from flask_login import current_user

from ..log import LogCharge
from ..mail import MailCharge


def user_logined_handler(sender, **data):
    """
    用户登录成功事件回调

    e.g.::

        event_user_logined.send(log_status=res)

    :param sender: 信号发送者/事件触发者
    :param data: 由发送者传递
    :return:
    """
    # 日志
    LogCharge.to_db({
        'log_status': 1 if data.pop('log_status', 0) else 0,
        'log_content': request.remote_addr,
    })

    # 邮件
    if current_user.email and current_app.config.get('MAIL_OPEN') and current_app.config.get('MAIL_PASSWORD'):
        MailCharge(
            subject='登录成功提醒: {}'.format(current_app.config.get('APP_NAME')),
            recipients=[current_user.email],
            extra_headers={'X-Priority': '1'}
        ).html_template(**data).text_template(**data).send_mail()
