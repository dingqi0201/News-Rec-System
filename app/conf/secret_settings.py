"""
    secret_settings.py
    ~~~~~~~~
    生产环境配置项(必须)

    :author: Fufu, 2019/9/2
"""
from . import get_environ, set_environ

##########
# CORE
##########

# 16-byte 密钥
SECRET_KEY = WTF_CSRF_SECRET_KEY = b';;\xff\xf7ok\x01&\x55~\xe2\xa6\x0bYff'

##########
# OAuth2
##########

# 正式环境的 OAuth 配置
OA_CLIENT_ID = 'ffpy123glfxxxdabci3loln1xunyouff'
OA_CLIENT_SECRET = get_environ('PYADMIN_OAUTH_SECRET', key=SECRET_KEY)
OA_API_BASE_URL = 'http://oa.xxx.com/oauth2/'
OA_AUTHORIZE_URL = 'http://oa.xxx.com/oauth2/authorize/'
OA_ACCESS_TOKEN_URL = 'http://oa.xxx.com/oauth2/access_token/'
OA_REFRESH_TOKEN_URL = 'http://oa.xxx.com/oauth2/refresh_token/'
# 允许 HTTP
set_environ('AUTHLIB_INSECURE_TRANSPORT', '1')

##########
# DB
##########

SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:123456@127.0.0.1:3306/news_flask?charset=utf8mb4'.format(get_environ('PYADMIN_DBPASS', key=SECRET_KEY))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_recycle': 3599,
    'pool_size': 100,
    'max_overflow': -1,
}

##########
# Mail
##########

MAIL_OPEN = False
MAIL_SERVER = 'smtp.qq.com'
MAIL_PROT = 465
MAIL_USE_TLS = True
MAIL_USERNAME = 'yfufuok@qq.com'
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = 'yfufuok@qq.com'
