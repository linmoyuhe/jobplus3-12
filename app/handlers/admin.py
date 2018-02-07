from flask import Blueprint, render_template, url_for, request, current_app, redirect, fllash
from forms.py import RegisterForm, CandidateForm, CompanyForm
from models.py import db, User, Job
admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
def index():
    return render_template('admin/index.html')

@admin.route('/users')
page = request.args.get('page',default = 1, type = int) 
pagination = User.query.paginate(
        page = page,
        per_page = current_app.config[''ADMIN_PER_PAGE],
        ERROR_OUT = False)
return render_template('admin/users.html', pagination = pagination)

@admin.route('users/creater_user', methods = ['GET', 'POST'])
def create_user():
    form = RegisterForm()
    if if form.is_submittted():
        form.create_user()
        flash('success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_user.html', form = form)

@admin.route('users/create_company', methods = ['GET', 'POST'])
def create_company():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_company.html', form = form)

@admin.route('/users/<int:user_id>/edit', methods = ['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_ot_404(user_id)
    if user.is_company:
        form = CompanyForm(obj = user)
    else:
        form = CandidateForm(obj = user)
    if form.validate_on_submit():
        form.update(user)
        flash('update success')
        return redirect(url_for('admin.user'))
    if user.is_company:
        form.site.data = user.detail.site
        form.description.data = user.detail.description
    return render_template('admin/edit_user.html', form = form, user = user)

@admin.route('/users/<int:user_id>/disable', method = ['GET', 'POST'])
def disable_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_disable:
        user.is_disable = False
        flash('disable user')
    else:
        user.is_disable = False
        flash('enable user')
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.users'))

@admin.route('/jobs')
def jobs():
    page = request.arg.get('page', default = 1, type = int)
    pagination = Job.query.paginate(
            page = page,
            per_page = current_app.config('ADMIN_PER_PAGE')
            error_out = Flase)
    return render_template('admin/jobs.html', pagination = pagination)

