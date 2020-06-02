from flask import (render_template, Blueprint, redirect,
                   url_for, request)
from belka.models import Website, Page


website = Blueprint('website', __name__)


@website.route('/index')
def index():
    website = Website.query.all()
    pages = Page.query.all()
    return render_template('main_website/index.html',
                           website=website,
                           pages=pages)
