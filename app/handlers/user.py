from flask import Blueprint, render_template, url_for


user = Blueprint('user', __name__, url_prefix='/user')