# -*- coding:utf-8 -*-
"""
    user.py
    ~~~~~~~~
    用户相关表

    2020/9/2
    :update: Fufu, 2019/12/20 User 表使用 id 字段配合 flask_login; 用户权限组关联使用 role_id; 日志增加 log_content
"""
from flask_login import UserMixin
from sqlalchemy import Column, Integer, SmallInteger, String, DateTime, func, BigInteger

from . import DBModel


class TBRole(DBModel):
    """角色表"""
    __tablename__ = 'ff_role'

    role_id = Column(Integer, autoincrement=True, primary_key=True, comment='自增主键')
    role = Column(String(20), unique=True, nullable=False, comment='角色标识, 如: admin, readonly')
    role_name = Column(String(30), nullable=False, comment='角色名称, 如: 管理员, 只读权限')
    role_allow = Column(String(5000), nullable=False, comment='允许的权限列表(蓝图/视图函数名), 逗号分隔')
    role_deny = Column(String(5000), server_default='', comment='禁止的权限(视图函数名), 最高优先级, 逗号分隔')


class TBUser(DBModel, UserMixin):
    """用户表"""
    __tablename__ = 'ff_user'

    id = Column(Integer, autoincrement=True, primary_key=True, comment='自增主键, UserMixin.get_id()')
    job_number = Column(Integer, unique=True, nullable=False, comment='工号, 重要')
    realname = Column(String(20), nullable=False, comment='姓名')
    email = Column(String(100), server_default='', comment='邮箱')
    role_id = Column(Integer, server_default='0', index=True, comment='角色标识ID')
    status = Column(SmallInteger, server_default='0', index=True, comment='状态: 1 正常, 0 禁用')


class TBLog(DBModel):
    """操作日志表"""
    __tablename__ = 'ff_log'

    log_id = Column(BigInteger, autoincrement=True, primary_key=True, comment='自增主键')
    log_time = Column(DateTime, index=True, server_default=func.now(), comment='日志写入时间')
    log_action = Column(String(50), index=True, nullable=False, comment='操作动作')
    log_operator = Column(String(20), index=True, nullable=False, comment='操作者姓名')
    log_content = Column(String(5000), server_default='', comment='操作详情')
    log_status = Column(SmallInteger, index=True, server_default='1', nullable=False, comment='操作是否成功')
