"""
    settings.py
    ~~~~~~~~
    通用配置项(必须)

    :author: Fufu, 2019/9/2
"""
##########
# CORE
##########

DEBUG = False
TIME_ZONE = 'Asia/Shanghai'
EXCEPTION_LOG_CODE = [500, 400]
EXCEPTION_DESC = {
    401: '未授权的请求',
    403: '请求权限不足',
    404: '页面未找到',
    405: '错误的请求方法',
    400: '错误请求, 请刷新重试',
    500: '系统服务异常',
    'dbapi': '数据库操作失败',
}

# 是否了使用 Nginx 等代理, 设置使用了几层代理, 影响获取客户端 IP (nginx + uwsgi 方式不影响)
# 如: script/nginx/pyadmin.conf + script/gunicorn/gunicorn.conf.py 时需要设置为 1, 或直接使用: get_real_ip('X-Real-IP')
# 如: 外边还有一层 Nginx 代理, 或有更多层的代理, 则需要指定层数, 如 2
# 此时 request.remote_addr 能正确获取的客户端 IP, 或不用下面的设置, 直接使用 get_real_ip('X-Forwarded-For')
PROXY_FIX_X_FOR = 0

##########
# LOG
##########

# logging.INFO = 20, CRITICAL = 50, ERROR = 40, WARNING = 30, DEBUG = 10
LOG_LEVEL = 20
# 单位 MB
LOG_MAXSIZE = 200
# 保留文件数
LOG_BACKUP = 30

##########
# APP
##########

# 可设置 APP_NAME 名称或 FLASK_CONFIG 环境变量值为: development / testing / production
APP_NAME = 'FF_PyAdmin'
# 系统管理员组(与数据库对应)
SYS_ROLE_ID = 1
# API 为 True 时所有请求都返回 JSON
API = False
# 保持键序
JSON_SORT_KEYS = False
# SESSION 生命周期
PERMANENT_SESSION_LIFETIME = 1440
# CSRF 生命周期
WTF_CSRF_TIME_LIMIT = 86400
# 运维接口白名单 IP
LOCAL_GW = ''
