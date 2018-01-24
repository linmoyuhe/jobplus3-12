#coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, IntegerField ,SelectField
from wtforms.validators import Length, Email, EqualTo, Required, URL, NumberRange, Regexp
from app.models import db, User, Company, Candidate
from flask_login import current_user
from flask import url_for


class LoginForm(FlaskForm):
	account = StringField('账号(用户名/邮箱/手机号)', validators=[Required(), Length(3, 24)])
	password = PasswordField('密码', validators=[Required(), Length(6, 24)])
	remember_me = BooleanField('记住我')
	submit = SubmitField('登录')

	def validate_account(self, field):
		if field.data:
			if not User.query.filter_by(username=field.data).first():
				if not User.query.filter_by(email=field.data).first():
					if not User.query.filter_by(phone=field.data).first():
						raise ValidationError('该账号还没有注册')

	def validate_password(self, field):
		user = User.query.filter_by(username=self.account.data).first()
		if not user:
			user = User.query.filter_by(email=self.account.data).first()
			if not user:
				user = User.query.filter_by(phone=self.account.data).first()
				if not user:
					raise ValidationError('该账号还没有注册')
		if not user.check_password(field.data):
			raise ValidationError('密码错误')


class RegisterForm(FlaskForm):
	username = StringField('用户名', validators=[Required(), Length(3, 24)])
	email = StringField('邮箱', validators=[Required(), Email()])
	phone = IntegerField('手机号', validators=[Required(), Regexp("^[1][34578][0-9]{9}$", message='手机号格式不正确')])
	password = PasswordField('密码', validators=[Required(), Length(6, 24)])
	repeat_pwd = PasswordField('重复密码', validators=[Required(), EqualTo('password')])
	role = SelectField('个人或企业', choices=[(10, '个人'),(20, '企业')])
	submit = SubmitField('注册')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('用户名已注册')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('邮箱已注册')

	def validate_phone(self, phone):
		if User.query.filter_by(phone=field.data).first():
			raise ValidationError('手机号已注册')

	def create_user(self):
		user = User(username=self.username.data, 
					email=self.email.data, 
					phone=self.phone.data, 
					password=self.password.data, 
					role=self.role.data)
		db.session.add(user)
		db.session.commit()
		return user


class CandidateForm(FlaskForm):

	name = StringField('姓名', validators=[Required(), Length(1, 32)])
	photo = StringField('照片')
	work_year = IntegerField('工龄')
	city = StringField('所在城市')
	education = SelectField('选择学历',
		choices=[
		('不限', '不限'),
		('本科', '本科'),
		('硕士', '硕士'),
		('博士','博士')
		])
	intro = TextAreaField('个人简介', validators=[Length(32,128)])
	cv_url = StringField('简历链接')
	submit = SubmitField('保存')

	def update_user(self, candidate):
		self.populate_obj(candidate)
        if self.education.data == '不限':
            candidate.education = 10
        elif self.education.data == '本科':
            candidate.education = 20
        elif self.education.data == '硕士':
            candidate.education = 30
        else:
            candidate.education = 40
		db.session.add(candidate)
		db.session.commit()
		return user


class CompanyForm(FlaskForm):
	"""docstring for CompanyForm"""
	name = StringField('公司名称', validators=[Required(), Length(1, 128)])
	city = StringField('地址',validators=[Required(), Length(1,128)])
	photo = StringField('Logo URL',validators=[Required()])
	website = StringField('官网', validators=[Required()])
	welfares = StringField('福利，用逗号隔开')
	intro = TextAreaField('描述', validators=[Required(), Length(1,1024)])

	submit = SubmitField('保存')

	def update_company(self, company):
		self.populate_obj(company)
		db.session.add(company)
		db.session.commit()
		return company
