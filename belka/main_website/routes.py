from flask import (render_template, Blueprint, redirect,
                   url_for, request, abort)
from flask_login import current_user
from belka.main_website.utils import (get_current_website,
                                      get_current_website_pages)
from belka.models import Post


website = Blueprint('website', __name__)


@website.route('/<website_name>/index')
def index(website_name):
    website = get_current_website(current_user.website_link_id)
    pages = get_current_website_pages(current_user.website_link_id)
    posts = Post.query.filter_by(post_page="index").all()
    return render_template('main_website/'+website_name+'/index.html',
                           website=website,
                           pages=pages, posts=posts)


@website.route('/<website_name>/<page_name>')
def go_to_page(page_name, website_name):
    website = get_current_website(current_user.website_link_id)
    pages = get_current_website_pages(current_user.website_link_id)
    posts = Post.query.filter_by(post_page=page_name).all()
    return render_template('main_website/'+website_name+'/'+page_name+'.html',
                           website=website,
                           title=page_name,
                           pages=pages, posts=posts)
