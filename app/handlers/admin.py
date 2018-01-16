from flask import Blueprint, render_template, url_for


admin = Blueprint('admin', __name__, url_prefix='/admin')
