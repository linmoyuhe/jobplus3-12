from flask import Blueprint, render_template, url_for


job = Blueprint('job', __name__, url_prefix='/job')