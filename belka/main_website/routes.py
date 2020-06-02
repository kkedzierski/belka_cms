from flask import (render_template, Blueprint, redirect,
                   url_for, request)
from belka.models import Website, Page


website = Blueprint('website', __name__)


@website.route('/<website_name>/index')
def index(website_name):
    website = Website.query.all()
    pages = Page.query.all()
    return render_template('main_website/'+website_name+'/index.html',
                           website=website,
                           pages=pages)


@website.route('/<website_name>/<page_name>')
def go_to_page(page_name, website_name):
    website = Website.query.all()
    pages = Page.query.all()
    return render_template('main_website/'+website_name+'/'+page_name+'.html',
                           website=website,
                           title=page_name,
                           pages=pages)
