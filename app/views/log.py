# -*- coding:utf-8 -*-
"""
    log.py
    ~~~~~~~~
    日志查询

    2020/9/21
"""
from flask import Blueprint, render_template
from flask_login import login_required

from ..forms import csrf
from ..forms.log import LogSearchForm, LogReportForm
from ..libs.exceptions import APISuccess
from ..services.auth import bgp_required
from ..services.log import LogCharge

bp_log = Blueprint('log', __name__, url_prefix='/log')


@bp_log.route('')
@login_required
def log_index():
    return render_template('log/index.html')


@bp_log.route('/list', methods=['POST'])
@login_required
def log_list():
    form = LogSearchForm().check()
    data = LogCharge.get_list(form.data, 500)
    return APISuccess(data)


@bp_log.route('/report', methods=['POST'])
@csrf.exempt
@bgp_required
def log_report(bgp_info):
    form = LogReportForm().check()
    form.data.update({'log_operator': bgp_info['bgp_ip']})
    LogCharge.to_db(form.data)

    return APISuccess()


@bp_log.route('/csrf_demo', methods=['POST'])
def csrf_demo():
    """WTF_CSRF_ENABLED = True 时, 会返回 400 错误"""
    return 'Be: flask_wtf.csrf.CSRFError: 400 Bad Request: The CSRF token is missing.'


@bp_log.route('/csrf_exempt_demo', methods=['POST'])
@csrf.exempt
def csrf_exempt_demo():
    """上例的正确使用方式"""
    return 'Be: csrf_exempt_demo'
