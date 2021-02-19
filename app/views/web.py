"""
    bp_web.py
    ~~~~~~~~
    主页

    :author: Fufu, 2019/9/2
"""
import os

from authlib.common.errors import AuthlibBaseError
from flask import (Blueprint, current_app, send_from_directory, redirect, url_for,
                   render_template, session)
from flask_login import logout_user, login_required
from requests.exceptions import RequestException

from ..forms import csrf
from ..libs.exceptions import APISuccess
from ..models.dao.mssql import MSSQL
from ..models.dao.mysql import MYSQL
from ..services.auth import oauth, chk_user_login, set_user_login
from ..services.events import event_async_with_app_demo

bp_web = Blueprint('web', __name__)
csrf.exempt(bp_web)


@bp_web.route('/')
@login_required
def web_index():
    """主页"""
    return render_template('index.html')


@bp_web.route('/news')
@login_required
def web_news():
    """新闻详情页"""
    return render_template('news.html')


@bp_web.route('/login')
def web_login():
    """登录页"""
    return render_template('login.html')


@bp_web.route('/authorize')
def web_authorize():
    """OAuth 登录跳转"""

    # TODO: (演示使用, 自动登录), 请删除并配置自己的认证方式, OAuth2或账密系统
    set_user_login({
        'job_number': 7777,
        'realname': 'Fufu'
    })
    return redirect(url_for('web.web_index'))

    # OAuth 认证
    redirect_uri = url_for('web.web_authorized', _external=True)
    return oauth.OA.authorize_redirect(redirect_uri)


@bp_web.route('/authorized')
def web_authorized():
    """OAuth 登录认证"""
    try:
        token = oauth.OA.authorize_access_token()
    except (AuthlibBaseError, RequestException):
        return redirect(url_for('web.web_authorize'))

    # 用户身份校验
    chk_user_login(token)

    return redirect(url_for('web.web_index'))


@bp_web.route('/logout')
@login_required
def web_logout():
    """退出登录"""
    logout_user()
    session.clear()

    return redirect(url_for('web.web_index'))


@bp_web.route('/favicon.ico')
def web_favicon():
    """浏览器地址栏图标"""
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@bp_web.route('/async_signal_demo')
def web_async_signal_demo():
    """异步信息示例"""
    event_async_with_app_demo.send(current_app._get_current_object(), mydata='view.data')
    return render_template('base-msg.html', e={'content': '页面已返回, 5秒后查看控制台日志'})


@bp_web.route('/show_asn_cache')
def web_show_asn_cache():
    """显示 ASN 缓存"""
    return current_app.config.get('ASN_LIST', set())


@bp_web.route('/result_tpl')
def web_result_tpl():
    """访问第三方提供的数据库示例"""
    # 原始 SQL 查询, 或执行存储过程
    # 因依附于 SQLAlchemy, 各数据库请求方式相同
    # 原生方式参考 result_tpl 的实现, 注: MSSQL 先安装 pyodbc 或 pymssql; Oracle 先配置环境, 安装 cx_Oracle
    res = MYSQL.result_tpl('other_mysqldb_test', {'num': 5}, ['工号', '姓名'])
    # res = MSSQL.result_tpl('mssql_case1_test')
    # res = OCI.result_tpl('...')
    return APISuccess(res)
