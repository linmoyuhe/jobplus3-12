from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


db = SQLAlchemy()


class Base(db.Model):
	__abstract__ = True
	create_at = db.Column(db.DateTime, default=datetime.utcnow)
	update_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# 登录用户
class User(Base, UserMixin):
	__tablename__ = 'user'

	# 求职者
	ROLE_CANDIDATE = 10
	# 招聘企业
	ROLE_COMPANY = 20
	# 管理员
	ROLE_ADMIN = 30

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32), unique=True, index=True, nullable=False)
	email = db.Column(db.String(64), unique=True, index=True, nullable=False)
	phone = db.Column(db.Integer, unique=True, index=True, nullable=False)
	_password = db.Column('password', db.String(256), nullable=False)
	# 登录用户类别
	role = db.Column(db.SmallInteger, default=ROLE_CANDIDATE)

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
		return self.role == self.ROLE_ADMIN

	@property
	def is_company():
		return self.role == self.ROLE_COMPANY

	@property
	def is_candidate():
		return self.role == self.ROLE_CANDIDATE


# 求职者-与登录用户是一对一的关系
class Candidate(Base):
	__tablename__ = 'candidate'

	# 学历不限
	EDUCATION_NO_lIMITED = 0
	# 本科以下
	EDUCATION_COLLEGE_BELOW = 10
	# 本科
	EDUCATION_COLLEGE = 20
	# 硕士
	EDUCATION_MASTER = 30
	# 博士
	EDUCATION_PHD = 40

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
	# 姓名
	name = db.Column(db.String(32), index=True, nullable=False)
	# 头像
	photo = db.Column(db.String(256))
	# 介绍
	intro = db.Column(db.String(256))
	# 城市
	city = db.Column(db.String(24))
	# 简历url
	cv_url = db.Column(db.String(256))
	# 工作年龄
	work_year = db.Column(db.Integer, default=0)
	# 期望薪资(单位：K)
	expected_salary = db.Column(db.SmallInteger)
	# 教育
	education = db.Column(db.SmallInteger, default=EDUCATION_NO_lIMITED)
	# 对应登录用户
	user = db.relationship('User', uselist=False, backref='candidate')

	def __repr__(self):
		return "<Candidate:{}>".format(self.name)


# 企业-与登录用户是一对一的关系
class Company(Base):
	__tablename__ = 'comnpany'

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
	# 名称
	name = db.Column(db.String(32), index=True, nullable=False)
	# logo
	photo = db.Column(db.String(256))
	# 介绍
	intro = db.Column(db.String(256))
	# 城市
	city = db.Column(db.String(24))
	# 官网
	website = db.Column(db.String(256))
	# 福利
	welfares = db.Column(db.String(256))
	# 对应登录用户
	user = db.relationship('User', uselist=False, backref='company')

	def __repr__(self):
		return "<Company:{}>".format(self.name)


# 职位
class Job(Base):
	__tablename__ = 'job'

	# 学历不限
	EDUCATION_NO_lIMITED = 0
	# 本科以下
	EDUCATION_COLLEGE_BELOW = 10
	# 本科
	EDUCATION_COLLEGE = 20
	# 硕士
	EDUCATION_MASTER = 30
	# 博士
	EDUCATION_PHD = 40

	id = db.Column(db.Integer, primary_key=True)
	# 职位名称
	name = db.Column(db.String(32), index=True, nullable=False)
	# 职位描述
	description = db.Column(db.String(256))
	# 职位要求
	requirements = db.Column(db.String(256))
	# 职位标签，多个用逗号隔开，最多10个
	tags = db.Column(db.String(128))
	# 所在城市
	city = db.Column(db.String(24))
	# 最小薪资(单位：K)
	min_salary = db.Column(db.SmallInteger, nullable=False)
	# 最大薪资(单位：K)
	max_salary = db.Column(db.SmallInteger, nullable=False)
	# 工作年限要求(0为不限)
	work_year_require = db.Column(db.SmallInteger)
	# 教育要求(默认不限)
	education_require =  db.Column(db.SmallInteger, default=EDUCATION_NO_lIMITED)
	# 企业 与 职位 是一对多的关系
	company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
	# backref：反向引用，相当于给Company表动态的添加jobs字段对应其所含有的Job实例
	# dynamic：用于一对多或多对多的关系中，访问属性后并不会直接返回结果，而是返回一个query对象，需要执行相应方法才可获取对象
	company = db.relationship('Company', uselist=False, backref=db.backref('jobs', lazy='dynamic'))
	# 查看人数
	view_count = db.Column(db.Integer, default=0)
	# 是否正在招聘
	is_open = db.Column(db.Boolean, default=True)

	def __repr__(self):
<<<<<<< HEAD
		return "<Job:{}>".format(self.name)

	@property
	def tag_list(self):
		return self.tags.split(',')


# 投递
class Delivery(Base):
	__tablename__ = 'delivery'

	# 等待企业审核
	STATUS_WAITTING = 1
	# 被拒绝
	STATUS_REJECT = 2
	# 被接受
	STATUS_ACCEPT = 3

	id = db.Column(db.Integer, primary_key=True)
	job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete='SET NULL'))
	candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id', ondelete='SET NULL'))
	comnpany_id = db.Column(db.Integer, db.ForeignKey('conpany.id', ondelete='SET NULL'))
	# 投递状态
	status = db.Column(db.SmallInteger, default=STATUS_WAITTING)
	# 企业回应
	response = db.Column(db.String(256))

	@property
	def job(self):
		return Job.query.get(self.job_id)

	@property
	def candidate(self):
		return Candidate.query.get(self.candidate_id)

	@property
	def company(self):
		return Company.query.get(self.comnpany_id)
=======
		return "<Job:{}>".format(self.name)
>>>>>>> fix models
