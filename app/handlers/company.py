from flask import Blueprint, render_template, url_for


company = Blueprint('company', __name__, url_prefix='/company')