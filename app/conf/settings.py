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
# 获取客户端 IP 的标头, 空串表示使用 request.remote_addr 获取, 详见: libs/helper::get_real_ip()
# 如: script/nginx/pyadmin.conf + script/gunicorn/gunicorn.conf.py 时启用 'X-Real-IP'
# 如用 uwsgi 部署 或 python3 dev.py 调试时则不需要下列配置, 或配置为空串
# REAL_IP_HEADER = 'X-Real-IP'
# REAL_IP_HEADER = 'X-Forwarded-For'

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
