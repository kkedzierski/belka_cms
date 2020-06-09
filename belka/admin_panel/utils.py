from flask_login import current_user
from belka.models import Website, WebsiteLink, Page, User
import os
import shutil
import enum
import secrets
from PIL import Image
from flask import current_app


def get_current_website(website_link_id):
    website_link = WebsiteLink.query.filter_by(id=website_link_id).first()
    if website_link is not None:
        website = Website.query.filter_by(id=website_link.website_id).first()
        return website
    else:
        return None


def get_website_by_id(website_id):
    website = Website.query.filter_by(id=website_id).first()
    return website


def get_current_website_pages(website_link_id):
    website = get_current_website(website_link_id)
    pages = Page.query.filter_by(website_id=website.id).all()
    return pages


def is_user_website_created(current_user_id):
    user = User.query.filter_by(id=current_user_id).first()
    print(user)
    if current_user.is_authenticated and user.website_link_id is None:
        return False
    else:
        return True


def go_to_main_website_templates():
    file_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(file_dir)
    new_path = os.path.join(parent_dir, 'templates/main_website')
    return new_path


def create_new_empty_page(dir_name, page_name):
    page_template = """{% extends 'main_website/website_layout.html' %}
{% block content %}{% for post in posts %}
<article class="media content-section">
  <img class="rounded-circle article-img" src="{{ url_for('static', filename='images/' + post.author.image_file) }}">
  <div class="media-body">
    <div class="article-metadata">
      <a>{{ post.author.username }}</a>
      <small class="text-muted">{{ post.date_posted.strftime('%Y-%m-%d') }}</small>
    </div>
    <h2 class="post-title">{{ post.title }}</h2>
    <p class="post-content article-content">{{ post.content }}</p>
  </div>
</article>
{% endfor %}{% endblock content %}"""
    go_to_main_website_templates()
    path_to_save_page = os.path.join(go_to_main_website_templates(),
                                     dir_name)
    new_page_path = os.path.join(path_to_save_page, page_name+".html")
    with open(new_page_path, "w") as file:
        file.write(page_template)


def delete_page(page_name, website_link_id):
    website = get_current_website(website_link_id)
    page_path = os.path.join(go_to_main_website_templates(),
                             website.title, page_name+".html")
    if page_path is not None:
        os.remove(page_path)
    else:
        print("File doesn't exist")


def change_page_name_in_html_file(old_page_name, new_page_name,
                                  current_user_id):
    website = get_current_website(current_user_id)
    old_page_path = os.path.join(go_to_main_website_templates(),
                                 website.title, old_page_name+".html")
    new_page_path = os.path.join(go_to_main_website_templates(),
                                 website.title, new_page_name+".html")
    os.rename(old_page_path, new_page_path)


def create_directory(dir_name, path=go_to_main_website_templates()):
    directory_path = os.path.join(path, dir_name)
    os.mkdir(directory_path)


def is_directory_exist(dir_name, path=go_to_main_website_templates()):
    directory_path = os.path.join(path, dir_name)
    return True if os.path.isdir(directory_path) else False


def delete_directory(dir_name, path=go_to_main_website_templates()):
    directory_path = os.path.join(path, dir_name)
    shutil.rmtree(directory_path, ignore_errors=True)


def change_directory_name(dir_name, new_dir_name,
                          path=go_to_main_website_templates()):
    directory_path = os.path.join(path, dir_name)
    new_directory_path = os.path.join(path, new_dir_name)
    os.rename(directory_path, new_directory_path)


def create_home_page(dir_name):
    page_template = """{% extends 'main_website/website_layout.html' %}
{% block content %}{% for post in posts %}
<article class="media content-section">
  <img class="rounded-circle article-img" src="{{ url_for('static', filename='images/' + post.author.image_file) }}">
  <div class="media-body">
    <div class="article-metadata">
      <a>{{ post.author.username }}</a>
      <small class="text-muted">{{ post.date_posted.strftime('%Y-%m-%d') }}</small>
    </div>
    <h2>{{ post.title }}</h2>
    <p class="article-content">{{ post.content }}</p>
  </div>
</article>
{% endfor %}{% endblock content %}"""
    go_to_main_website_templates()
    path_to_save_page = os.path.join(go_to_main_website_templates(),
                                     dir_name)
    new_page_path = os.path.join(path_to_save_page, "index.html")
    with open(new_page_path, "w") as file:
        file.write(page_template)


class UserRoles(enum.Enum):
    admin = 1
    editor = 2
    author = 3


def get_user_role(role):
    for roles in UserRoles:
        if role == roles.name:
            return role
    return None


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images',
                                picture_fn)

    output_size = (125, 125)
    resized_image = Image.open(form_picture)
    resized_image.thumbnail(output_size)
    resized_image.save(picture_path)

    return picture_fn
