from flask_login import current_user
from belka.models import Website, WebsiteLink, User
import enum


def get_current_website(website_link_id):
    website_link = WebsiteLink.query.filter_by(id=website_link_id).first()
    if website_link is not None:
        website = Website.query.filter_by(id=website_link.website_id).first()
        return website
    else:
        return None


def is_user_website_created(current_user_id):
    user = User.query.filter_by(id=current_user_id).first()
    print(user)
    if current_user.is_authenticated and user.website_link_id is None:
        return False
    else:
        return True


class UserRoles(enum.Enum):
    admin = 1
    editor = 2
    author = 3
