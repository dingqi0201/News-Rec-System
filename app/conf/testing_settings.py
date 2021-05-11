"""
    testing_settings.py
    ~~~~~~~~
    测试环境配置项(高优先级)
    BDD 或单元测试时使用

    e.g.::

        from app import create_app
        app = create_app(config_name='testing')

    2020/9/2
"""

##########
# CORE
##########

TESTING = True
WTF_CSRF_ENABLED = False

##########
# DB
##########

# SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:123456@127.0.0.1:3306/news_flask?charset=utf8mb4'
