# -*- coding:utf-8 -*-
"""
    observer.py
    ~~~~~~~~
    自定义信号, 观察者

    2020/12/20
"""
from blinker import Signal, ANY


class Observer:
    """自定义信号"""

    app = None
    _observers = []

    def init_app(self, app):
        """绑定 Flask APP"""
        self.app = app
        for ob in self._observers:
            sender = ob.get('sender', ANY)
            if sender == 'ANY':
                sender = ANY
            elif sender == 'APP':
                sender = app
            ob['signal_name'].connect(ob['receiver'], sender=sender)

    def add(self, signal_name, receiver, sender=ANY):
        """
        增加订阅者

        e.g.::

            def callback_function_for_app(sender, **kwargs):
                pass
            def callback_function_for_all(sender, **kwargs):
                pass
            my_signal = signal('test')
            observer.add(my_signal, callback_function_for_app, 'APP')
            observer.add(my_signal, callback_function_for_all)

        :param signal_name: 订阅的主题, 信号
        :param receiver: 订阅者回调方法
        :param sender: ANY, 'ANY' 面向所有发布者(默认), 'APP', current_app._get_current_object() 当前 APP
        :return:
        """
        if isinstance(signal_name, Signal) and hasattr(receiver, '__call__'):
            self._observers.append({
                'signal_name': signal_name,
                'receiver': receiver,
                'sender': sender,
            })

    def add_via(self, signal_name, sender=ANY):
        """
        增加订阅者, observer.add 的装饰器方法

        e.g.::

            @observer.add_via(my_signal, 'APP')
            def callback_function_for_app(sender, **kwargs):
                pass

        :param signal_name:
        :param sender:
        :return:
        """

        def decorator(fn):
            self.add(signal_name, fn, sender)
            return fn

        return decorator
