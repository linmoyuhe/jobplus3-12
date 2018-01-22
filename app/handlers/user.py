#coding:utf-8
from flask import Blueprint, render_template, redirect, flash, url_for
from jobplus.models import db, User, Candidate
from .forms import CandidateForm
from flask_login import login_required, current_user
user = Blueprint('user', __name__, url_prefix="/user")


@user.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	user = Candidate.query.get_or_404(current_user.candidate.id)
	form = CandidateForm(obj=candidate)
	if form.validate_on_submit():
		form.update_user(candidate)
		flash('保存成功', 'success')
		return redirect(url_for('user.profile'))
	return render_template('user/profile.html', form=form)
