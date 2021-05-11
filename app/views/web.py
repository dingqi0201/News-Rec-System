import os

from authlib.common.errors import AuthlibBaseError
from flask import (Blueprint, current_app, send_from_directory, redirect, url_for,
                   render_template, session)
from flask_login import logout_user, login_required
from requests.exceptions import RequestException

from app.models.news import HotHomeNews, TESTNews

from app.src.model_loader import load_model
from ..forms import csrf
from ..libs.exceptions import APISuccess
from ..models.dao.mysql import MYSQL
from ..services.auth import oauth, chk_user_login, set_user_login
from ..services.events import event_async_with_app_demo
from ..models import db

bp_web = Blueprint('web', __name__)
csrf.exempt(bp_web)


@bp_web.route('/')
@login_required
def web_index():
    """主页"""

    news = db.session.query(HotHomeNews).to_dicts
    home = list()
    hot = list()
    for i in news:
        if i['hot'] == 1:
            hot.append(i)
        else:
            home.append(i)

    return render_template('index.html', hot=hot, home=home)


@bp_web.route('/news/<id>', methods=['GET'])
@login_required
def web_news(id):
    """新闻详情页
    1. 浏览记录写raw_history.txt
    2. 热点表不更新，首页表不更新
    3. 调用模型
    4. 得分对应关系以及排序
    5. 查询
    """
    # 根据前端点击从TESTNews表中找到所点击的新闻
    clicked_news = db.session.query(HotHomeNews).get(id).to_dict
    print(clicked_news)

    # 将已点击的新闻写进raw_history.txt
    writer = open("app/real_data/raw_history.txt", 'a', encoding='utf-8')
    writer.write(
        '%s\t%s\t%s\t%s\n' % (0, clicked_news["news_id"], clicked_news["news_words"], clicked_news["month"]))
    writer.close()

    # 调用模型，喂入数据，得到预测得分
    res = load_model()

    # 将候选新闻id和其得分写成dict格式
    news_dict = dict()
    for index, i in enumerate(res):
        news_dict[index + 10000] = i

    # 将dict中已经点击的新闻去掉，即不会推荐已经点击过的新闻
    clicked_id = []
    reader = open("app/real_data/raw_history.txt", encoding='utf-8')
    for line in reader:
        array = line.strip().split('\t')
        news_id = array[1]
        clicked_id.append(eval(news_id))
    reader.close()

    for i in list(news_dict.keys()):
        if i in clicked_id:
            news_dict.pop(i)

    # 将候选新闻按得分由高到低排序，并取前5个写入recommend_news
    result_dict = sorted(news_dict.items(), key=lambda d: d[1], reverse=True)
    recommend_news = []
    print("==============index result_dict[:5]==============\n", result_dict[:5])
    for i in result_dict[:5]:
        recommend_news.append(db.session.query(TESTNews).get(i[0]).to_dict)
    # print(recommend_news)

    return render_template('news.html', recommend_news=recommend_news, clicked_news=clicked_news)


@bp_web.route('/news/recommend/<id>', methods=['GET'])
@login_required
def recommend_news(id):
    # 根据前端点击从TESTNews表中找到所点击的新闻
    clicked_news = db.session.query(TESTNews).get(id).to_dict
    print(clicked_news)

    # 将已点击的新闻写进raw_history.txt
    writer = open("app/real_data/raw_history.txt", 'a', encoding='utf-8')
    writer.write(
        '%s\t%s\t%s\t%s\n' % (0, clicked_news["news_id"], clicked_news["news_words"], 3))
    writer.close()

    # 调用模型，喂入数据，得到预测得分
    res = load_model()

    # 将候选新闻id和其得分写成dict格式
    news_dict = dict()
    for index, i in enumerate(res):
        news_dict[index + 10000] = i

    # 将dict中已经点击的新闻去掉，即不会推荐已经点击过的新闻
    clicked_id = []
    reader = open("app/real_data/raw_history.txt", encoding='utf-8')
    for line in reader:
        array = line.strip().split('\t')
        news_id = array[1]
        clicked_id.append(eval(news_id))
    reader.close()

    for i in list(news_dict.keys()):
        if i in clicked_id:
            news_dict.pop(i)

    # 将候选新闻按得分由高到低排序，并取前5个写入recommend_news
    result_dict = sorted(news_dict.items(), key=lambda d: d[1], reverse=True)
    print("==============recommend result_dict[:5]==============\n", result_dict[:5])
    recommend_news = []
    for i in result_dict[:5]:
        recommend_news.append(db.session.query(TESTNews).get(i[0]).to_dict)
    # print(recommend_news)

    return render_template('news.html', recommend_news=recommend_news, clicked_news=clicked_news)


@bp_web.route('/login')
def web_login():
    """登录页"""
    # 首先清理history数据

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
