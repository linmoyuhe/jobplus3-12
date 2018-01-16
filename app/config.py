# 域名 和 端口 可根据个人环境改变
DOMAIN_NAME = 'root@localhost'
PORT = '3306'

class BaseConfig(object):
	SECRET_KEY = 'wubba lubba dub dub'


class DevelopementConfig(BaseConfig):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DOMAIN_NAME + ':' + PORT + '/jobplus?charset=utf8'


class ProductionConfig(BaseConfig):
	DEBUG = False


class TestingConfig(BaseConfig):
	DEBUG = False


configs = {
	'development':DevelopementConfig,
	'production': ProductionConfig,
	'testing': TestingConfig
}