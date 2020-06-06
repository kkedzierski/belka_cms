from flask_login import current_user
from belka.models import Website, WebsiteLink
import enum


def get_current_website(current_user_id):
    website_link = WebsiteLink.query.filter_by(user_id=current_user_id).first()
    if website_link is not None:
        website = Website.query.filter_by(id=website_link.website_id).first()
        return website
    else:
        return None


def is_user_website_created(current_user_id):
    website = get_current_website(current_user_id)
    print(website)
    if current_user.is_authenticated and website is None:
        return False
    else:
        return True


class UserRoles(enum.Enum):
    admin = 1
    editor = 2
    author = 3
