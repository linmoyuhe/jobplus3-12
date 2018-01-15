class BaseConfig(object):
	SECRET_KEY = 'OENDA YOUWILLBE A AMAZING PYTHONENGINEER'

class DevelopementConfig(BaseConfig):
	DEBUG=True
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:wangyi@localhost:3306/jobplus?charset=utf8'

class ProductionConfig(BaseConfig):
	DEBUG=False

class TestingConfig(BaseConfig):
	DEBUG=False


configs = {
	'develope':DevelopementConfig,
	'product': ProductionConfig,
	'test': TestingConfig
}