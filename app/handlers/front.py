from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_user, logout_user, login_required


front = Blueprint('front', __name__)


@front.route('/')
def index():
	return render_template('front/index.html')


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
