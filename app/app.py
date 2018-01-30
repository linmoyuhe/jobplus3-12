from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import configs
from app.models import db, User
import datetime


def register_filters(app):

    @app.template_filter()
    def timesince(value):
        now = datetime.datetime.utcnow()
        diff = now - value
        if diff.days > 365:
            return '{}年前'.format(diff.days // 365)
        if diff.days > 30:
            return '{}月前'.format(diff.days // 30)
        if diff.days > 0:
            return '{}天前'.format(diff.days)
        if diff.seconds > 3600:
            return '{}小时前'.format(diff.seconds // 3600)
        if diff.seconds > 60:
            return '{}分钟前'.format(diff.seconds // 60)
        return '刚刚'

    @app.template_filter()
    def degree_require(value):
        if value >= 40:
            return '博士以上'
        if value >= 30:
            return '硕士以上'
        if value >= 20:
            return '本科以上'
        if value >= 10:
            return '大专以上'
        return '不限'


def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'


def register_blueprints(app):
    from .handlers import front, job, company, user, admin
    app.register_blueprint(front)
    app.register_blueprint(job)
    app.register_blueprint(company)
    app.register_blueprint(user)
    app.register_blueprint(admin)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    
    register_extensions(app) 
    register_blueprints(app)
    register_filters(app)
     
    return app
