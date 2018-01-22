#coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, IntegerField ,SelectField
from wtforms.validators import Length, Email, EqualTo, Required, URL, NumberRange
from app.models import db, User, Company, Candidate
from flask_login import current_user
from flask import url_for


class CandidateForm(FlaskForm):

	name = StringField('姓名', validators=[Required(), Length(1, 32)])
	photo = StringField('照片')
	work_year = IntegerField('工龄')
	city = StringField('住址')
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
