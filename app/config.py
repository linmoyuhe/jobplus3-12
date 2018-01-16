class BaseConfig(object):
	SECRET_KEY = 'wubba lubba dub dub'
	DOMAIN_NAME = 'root@localhost'
	PORT = '3306'


class DevelopementConfig(BaseConfig):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DOMAIN_NAME + ':' + PORT + '/jobplus?charset=utf8'


class ProductionConfig(BaseConfig):
	DEBUG = False


class TestingConfig(BaseConfig):
	DEBUG = False


configs = {
	'develope':DevelopementConfig,
	'product': ProductionConfig,
	'test': TestingConfig
}