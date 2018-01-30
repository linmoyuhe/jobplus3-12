from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_user, logout_user, login_required
from app.models import Job, Company, User


front = Blueprint('front', __name__)


@front.route('/')
def index():
	newest_jobs = Job.query.filter(Job.is_open == True).order_by(Job.create_at.desc()).limit(9)
    newest_companies = Company.query.order_by(Company.create_at.desc()).limit(8)
    return render_template('front/index.html', active='main', newest_jobs=newest_jobs, newest_companies=newest_companies)


@front.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('front/login.html')


@front.route('/register', methods=['GET', 'POST'])
def register():
	return render_template('front/register.html')


@front.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('.index'))
