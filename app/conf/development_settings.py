"""
    development_settings.py
    ~~~~~~~~
    开发环境配置项(最高优先级)

    先设置环境变量(FF_PyAdmin 是 settings.py 中设置的 APP_NAME):

    e.g.::

        1. Windows:
            set FF_PyAdmin=development
            echo %FF_PyAdmin%
        2. Linux:
            export FF_PyAdmin=development
            echo $FF_PyAdmin

    :author: Fufu, 2019/9/2
"""

##########
# CORE
##########

DEBUG = True
DEBUG_RESPONSE = True
JSON_AS_ASCII = False
WTF_CSRF_ENABLED = True
PROXY_FIX_X_FOR = 0

# 域名访问, 写 HOSTS: 127.0.0.1 ff.pyadmin
# SERVER_NAME = 'ff.pyadmin:777'

##########
# OAuth2
##########

OA_CLIENT_ID = 'ffpy123glfxxxdabci3loln1xunyouff'
OA_CLIENT_SECRET = 'kkpy123glfxxxdabci3loln1xunyouok'
OA_API_BASE_URL = 'http://oa/oauth2/'
OA_AUTHORIZE_URL = 'http://oa/oauth2/authorize/'
OA_ACCESS_TOKEN_URL = 'http://oa/oauth2/access_token/'
OA_REFRESH_TOKEN_URL = 'http://oa/oauth2/refresh_token/'

##########
# DB
##########

SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:123456@127.0.0.1:3306/news_flask?charset=utf8mb4'
# 调试模式, 显示 SQL
SQLALCHEMY_ECHO = False

# 额外访问的第三方数据库, 比如只读的表, 可以单独使用驱动
# Orcale 需要客户端环境, 从官网下载后解压即可
# Ref: https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html
OCI_LIB_PATH_NT = r'C:\Work\ff.server\ocix32v19'
OCI_LIB_PATH_POSIX = '/lib/ocix64v19'
OCI_LIB_PATH = OCI_LIB_PATH_POSIX
OCI_DATABASE_URI = 'oracle+cx_oracle://ocitest:ocitest@127.0.0.1:1521/spd'

# SQLServer 推荐使用 pyodbc, 各系统中文都显示正常
# Ref: https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server
# MSSQL_DATABASE_URI = 'mssql+pymssql://pytest:pytest@127.0.0.1:1433/XY_OA'
# MSSQL_DATABASE_URI = 'mssql+pyodbc://pytest:pytest@127.0.0.1:1433/XY_OA?driver=SQL+Server+Native+Client+10.0'
MSSQL_DATABASE_URI = 'mssql+pyodbc://pytest:pytest@127.0.0.1:1433/XY_OA?driver=ODBC+Driver+17+for+SQL+Server'

# MYSQL
MYSQL_DATABASE_URI = 'mysql+cymysql://root:123456@127.0.0.1:3306/news_flask?charset=utf8mb4'

# ASN 列表缓存
ASN_LIST = set()

# 数据请求模板, 用于数据相关配置分离, 需要可以做个后台管理, 示例见: /result_tpl
# { key 功能标识: (数据库连接标识, SQL 语句) }
QUERY_TPL = {
    'other_mysqldb_test': ('MYSQL_DATABASE_URI', '''SELECT job_number, realname FROM ff_user LIMIT [[.num.]]'''),
    'mssql_case1_test': ('MSSQL_DATABASE_URI', '''SELECT TOP 5 * FROM oa_user'''),
}

##########
# Mail
##########

MAIL_OPEN = False
MAIL_DEBUG = True
MAIL_SERVER = 'smtp.qq.com'
MAIL_PROT = 465
MAIL_USE_TLS = True
MAIL_USERNAME = 'yfufuok@qq.com'
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = 'yfufuok@qq.com'
