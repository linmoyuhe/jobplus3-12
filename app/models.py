from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
db = SQLAlchemy()

class Base(db.Model):
	__abstract__ = True
	create_at = db.Column(db.DateTime, default=datetime.utcnow)
	update_at = db.Column(db.DateTime, 
						  default=datetime.utcnow, 
						  onupdate=datetime.utcnow)

class User(Base, UserMixin):
	__tablename__ = 'user'

	# 三种用户
	# 普通用户
	# 企业用户
	# admin
	普通用户 = 10
	企业用户 = 20
	admin = 30

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32), unique=True, index=True, nullable=False)
	email = db.Column(db.String(64), unique=True, index=True, nullable=False)
	_password = db.Column('password', db.String(256), nullable=False)
	realname = db.Column(db.String(24))
	role = db.Column(db.SmallInteger, default=普通用户)
	# CASCADE 表示企业如果删除，对应的子账号也要删除
	company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
	company = db.relationship('Company')

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

	def is_company():
		return self.role == self.企业用户


class Job(Base):
	__tablename__ = 'job'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), unique=True, index=True, nullable=False)
	salary_range = db.Column(db.String(128))
	address = db.Column(db.String(256))
	exp_request = db.Column(db.String(32))
	degree_request = db.Column(db.String(32))
	description = db.Column(db.String(1024))
	job_request = db.Column(db.String(1024))
	company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
	company = db.relationship('Company')


class Company(Base):
	__tablename__ = 'company'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), unique=True, index=True, nullable=False)
	address = db.Column(db.String(256))
	logo_url = db.Column(db.String(256))
	website = db.Column(db.String(256), default="http://www.kernel.org")
	Slogan = db.Column(db.String(256))
	description = db.Column(db.String(1024))
