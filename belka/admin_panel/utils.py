from flask_login import current_user
from belka.models import Website, WebsiteLink, Page
import os
import shutil


def get_current_website(current_user_id):
    website_link = WebsiteLink.query.filter_by(user_id=current_user_id).first()
    if website_link is not None:
        website = Website.query.filter_by(id=website_link.website_id).first()
        return website
    else:
        return None


def get_current_website_pages(current_user_id):
    website = get_current_website(current_user_id)
    pages = Page.query.filter_by(website_id=website.id).all()
    return pages


def is_user_website_created(current_user_id):
    website = get_current_website(current_user_id)
    print(website)
    if current_user.is_authenticated and website is None:
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
{% block content %}{% endblock content %}"""
    go_to_main_website_templates()
    path_to_save_page = os.path.join(go_to_main_website_templates(),
                                     dir_name)
    new_page_path = os.path.join(path_to_save_page, page_name+".html")
    with open(new_page_path, "w") as file:
        file.write(page_template)


def delete_page(page_name, current_user_id):
    website = get_current_website(current_user_id)
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
{% block content %}{% endblock content %}"""
    go_to_main_website_templates()
    path_to_save_page = os.path.join(go_to_main_website_templates(),
                                     dir_name)
    new_page_path = os.path.join(path_to_save_page, "index.html")
    with open(new_page_path, "w") as file:
        file.write(page_template)
