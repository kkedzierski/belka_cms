from flask import flash
from flask_login import current_user
from belka.models import Website


def is_website_created():
    if current_user.is_authenticated and len(Website.query.all()) == 0:
        return False
    else:
        return True
