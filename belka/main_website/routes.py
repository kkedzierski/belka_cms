from flask import (render_template, Blueprint, redirect,
                   url_for, request)
from belka.models import Website


website = Blueprint('website', __name__)


@website.route('/index')
def index():
    website = Website.query.all()
    return render_template('main_website/index.html',
                           website=website)
