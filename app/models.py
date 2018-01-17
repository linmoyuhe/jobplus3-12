from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


db = SQLAlchemy()


class Base(db.Model):
	__abstract__ = True
	create_at = db.Column(db.DateTime, default=datetime.utcnow)
	update_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(Base, UserMixin):
	__tablename__ = 'user'

	ROLE_USER = 10
	ROLE_COMPANY = 20
	ROLE_ADMIN = 30

	EDUCATION_DEFAULT = 0
	EDUCATION_COLLEGE_BELOW = 10
	EDUCATION_COLLEGE = 20
	EDUCATION_COLLEGE_ABOVE = 30

	# 普通用户 和 企业用户 共有字段
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32), unique=True, index=True, nullable=False)
	email = db.Column(db.String(64), unique=True, index=True, nullable=False)
	moblie = db.Column(db.Integer, unique=True, index=True, nullable=False)
	_password = db.Column('password', db.String(256), nullable=False)
	role = db.Column(db.SmallInteger, default=ROLE_USER)
	photo = db.Column(db.String(256))
	description = db.Column(db.String(256))
	city = db.Column(db.String(24))
	# 普通用户对应简历url 企业用户对应公司网址
	extra_url = db.Column(db.String(256))
	# 普通用户特有字段(用于拓展删选job)
	work_year = db.Column(db.Integer, default=0)
	expected_salary = db.Column(db.SmallInteger)
	education = db.Column(db.SmallInteger, default=EDUCATION_DEFAULT)
	# 企业用户特有字段(一对多的关系)
	jobs = db.relationship('Job')

	def __repr__(self):
		return "<User:{}>".format(self.username)

	@property
	def password(self):
		return self._password

	@password.setter
	def password(self, orig_password):
		self._password = generate_password_hash(orig_password)

	def check_password(self, password):
		return check_password_hash(self._password, password)

	@property
	def is_admin():
		return self.role == self.admin

	@property
	def is_company():
		return self.role == self.ROLE_COMPANY


class Job(Base):
	__tablename__ = 'job'

	EDUCATION_DEFAULT = 0
	EDUCATION_COLLEGE_BELOW = 10
	EDUCATION_COLLEGE = 20
	EDUCATION_COLLEGE_ABOVE = 30

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), index=True, nullable=False)
	requirements = db.Column(db.String(256))
	description = db.Column(db.String(256))
	# 用于拓展删选job
	min_salary = db.Column(db.SmallInteger, nullable=False)
	max_salary = db.Column(db.SmallInteger, nullable=False)
  min_year_require = db.Column(db.SmallInteger)
  max_year_require = db.Column(db.SmallInteger)
	city = db.Column(db.String(24))
	education_require =  db.Column(db.SmallInteger, default=EDUCATION_DEFAULT)
	# 职位 与 企业 是一对一的关系
	company = db.relationship('User', uselist=False)
	
	def __repr__(self):
		return "<Job:{}>".format(self.name)

