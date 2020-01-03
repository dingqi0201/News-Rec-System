# -*- coding:utf-8 -*-
"""
    mail.py
    ~~~~~~~~
    邮件发送

    :author: Fufu, 2019/12/19
"""
from flask import current_app, render_template
from flask_mail import Mail, Message

from ..libs.helper import async_task

mail = Mail()


class MailCharge(Message):
    """邮件, 支持模板, 支持异步发送"""

    def html_template(self, template='mail/tpl.html', **kwargs):
        """
        渲染 HTML 内容模板
        赋值给 self.html

        :param template: 模板文件
        :param kwargs: 上下文件变量
        :return:
        """
        self.html = render_template(template, **kwargs)
        return self

    def text_template(self, template='mail/tpl.txt', **kwargs):
        """
        渲染纯文本内容模板
        赋值给 self.body

        :param template: 模板文件
        :param kwargs: 上下文件变量
        :return:
        """
        self.body = render_template(template, **kwargs)
        return self

    def send_mail(self, sync=False):
        """
        执行发送
        同步/异步(默认)

        :param sync: bool, True 同步发送
        :return:
        """
        if sync:
            mail.send(self)
        else:
            self._async_send(current_app._get_current_object())

    @async_task
    def _async_send(self, app):
        """异步发送邮件"""
        with app.app_context():
            mail.send(self)
