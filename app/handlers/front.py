from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_user, logout_user, login_required
from app.models import Job


front = Blueprint('front', __name__)


@front.route('/')
def index():
	page = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    return render_template('front/index.html', pagination=pagination)


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
