from flask_login import current_user
from belka.models import Website
import os


def is_website_created():
    if current_user.is_authenticated and len(Website.query.all()) == 0:
        return False
    else:
        return True


def go_to_main_website_templates():
    file_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(file_dir)
    new_path = os.path.join(parent_dir, 'templates/main_website')
    return new_path


def create_new_empty_page(page_name):
    page_template = """{% extends 'main_website/website_layout.html' %}
{% block content %}{% endblock content %}"""
    go_to_main_website_templates()
    new_page_path = os.path.join(go_to_main_website_templates(),
                                 page_name+".html")
    with open(new_page_path, "w") as file:
        file.write(page_template)


def delete_page(page_name):
    page_path = os.path.join(go_to_main_website_templates(),
                             page_name+".html")
    if page_path is not None:
        os.remove(page_path)
    else:
        print("File doesn't exist")


def change_page_name_in_html_file(old_page_name, new_page_name):
    old_page_path = os.path.join(go_to_main_website_templates(),
                                 old_page_name+".html")
    new_page_path = os.path.join(go_to_main_website_templates(),
                                 new_page_name+".html")
    os.rename(old_page_path, new_page_path)
