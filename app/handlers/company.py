#coding:utf-8
from flask import Blueprint, render_template, url_for, current_app, flash, redirect, request
from jobplus.models import db, Company
from flask_login import login_required, current_user
from .forms import CompanyForm

company = Blueprint('company', __name__, url_prefix="/company")

@company.route('/admin/profile', methods=['GET', 'POST'])
@login_required
def profile():
	company = Company.query.get_or_404(current_user.company.id)
	form = CompanyForm(obj=company)
	if form.validate_on_submit():
		form.update_company(company)
		flash('保存成功', 'success')
		return redirect(url_for('company.profile'))
	return render_template('company/profile.html', form=form)
