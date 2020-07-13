# -*- coding:utf-8 -*-
"""
    bgp.py
    ~~~~~~~~
    BGP 相关表

    :author: Fufu, 2019/9/2
"""
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Numeric, Float

from . import DBModel


class TBASN(DBModel):
    """AS 号信息表"""
    __tablename__ = 'ff_asn'

    asn = Column(Integer, primary_key=True, comment='主键, ASN(Autonomous System Number)')
    asn_desc = Column(String(500), nullable=False, comment='ASN 描述')


class TBBGP(DBModel):
    """BGP 信息表"""
    __tablename__ = 'ff_bgp'

    bgp_ip_id = Column(BigInteger, autoincrement=True, primary_key=True, comment='自增主键')
    bgp_ip = Column(String(40), unique=True, nullable=False, comment='BGP 管理 IP')
    bgp_asn = Column(Integer, index=True, nullable=False, comment='BGP 所属 ASN')
    bgp_desc = Column(String(500), nullable=False, comment='BGP 服务器描述')
    bgp_update = Column(DateTime, index=True, comment='最后更新成功时间')
    bgp_test_decimal = Column(Numeric(13, 2), server_default='0', nullable=False, comment='(返回数据集前时隐藏该字段)')
    bgp_test_float = Column(Float, server_default='1', comment='(测试浮点数)')
    bgp_test_hide1 = Column(Float, server_default='2', comment='(前端自动表格测试指定隐藏)')
    bgp_test_hide2 = Column(Float, server_default='3', comment='(前端自动表格测试)')
