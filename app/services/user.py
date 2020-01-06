# -*- coding:utf-8 -*-
"""
    user.py
    ~~~~~~~~
    用户管理和用户权限分配

    :author: Fufu, 2019/9/21
    :update: Fufu, 2019/12/20 使用 role_id 关联用户权限组
"""
from sqlalchemy import desc

from .events import event_sys_admin
from ..libs.exceptions import APIFailure
from ..models import db
from ..models.user import TBUser, TBRole


class UserCharge:
    """User 相关数据表操作"""

    @staticmethod
    def get_list(job_number=0, realname=''):
        """
        获取用户列表(暂未分页)

        :param job_number: int
        :param realname: str
        :return: list
        """
        q = db.session. \
            query(TBUser, TBRole). \
            outerjoin(TBRole, TBUser.role_id == TBRole.role_id). \
            order_by(desc(TBUser.status))

        if job_number:
            q = q.filter(TBUser.job_number == job_number)
        if realname:
            q = q.filter(TBUser.realname == realname)

        return q.to_dicts

    @staticmethod
    def authorize(data, as_api=False):
        """
        更新用户数据

        :param data: dict
        :param as_api: bool, True 入库失败返回 APIException
        :return:
        """
        res = TBUser().replace(data)
        event_sys_admin.send(log_status=res, log_content=data)
        if not res and as_api:
            raise APIFailure('用户授权失败')

        return res

    @staticmethod
    def deny(job_number, as_api=False):
        """
        禁用用户

        :param job_number: int
        :param as_api: bool
        :return:
        """
        res = TBUser.query.filter_by(job_number=job_number).update({'status': 0, 'role_id': 0})
        event_sys_admin.send(log_status=res, log_content=job_number)
        if not res and as_api:
            raise APIFailure('禁用用户失败')

        return res
