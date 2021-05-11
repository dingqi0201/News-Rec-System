# -*- coding:utf-8 -*-
"""
    for bgp.feature
    ~~~~~~~~

    2020/10/9
"""
from behave import *
from flask import Response


@given('输入BGP-IP, ASN和描述 "{bgp_ip}", "{bgp_asn}", "{bgp_desc}", "{bgp_test_float}"')
@given('输入BGP-IP和描述, ASN错误 "{bgp_ip}", "{bgp_asn}", "{bgp_desc}", "{bgp_test_float}"')
@given('BGP-IP输入错误 "{bgp_ip}", "{bgp_asn}", "{bgp_desc}", "{bgp_test_float}"')
@given('浮点数输入错误 "{bgp_ip}", "{bgp_asn}", "{bgp_desc}", "{bgp_test_float}"')
def step_impl(ctx, bgp_ip, bgp_asn, bgp_desc, bgp_test_float):
    ctx.bgp_ip = bgp_ip
    ctx.bgp_asn = bgp_asn
    ctx.bgp_desc = bgp_desc
    ctx.bgp_test_float = bgp_test_float


@when('执行添加BGP操作')
def step_impl(ctx):
    ctx.resp = ctx.client.post('/bgp/add', data={
        'bgp_ip': ctx.bgp_ip,
        'bgp_asn': ctx.bgp_asn,
        'bgp_desc': ctx.bgp_desc,
        'bgp_test_float': ctx.bgp_test_float,
    })


@then('BGP-IP添加成功')
def step_impl(ctx):
    assert isinstance(ctx.resp, Response)
    assert ctx.resp.status_code == 200
    res = ctx.resp.json
    print('bgp_add: {}'.format(res))
    assert res['ok'] == 1


@then('BGP添加失败')
def step_impl(ctx):
    assert isinstance(ctx.resp, Response)
    assert ctx.resp.status_code == 200
    res = ctx.resp.json
    print('bgp_add: {}'.format(res))
    assert res['ok'] == 0
    assert res['err_code'] > 0
    assert res['msg']
