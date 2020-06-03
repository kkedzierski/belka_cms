from belka.models import WebsiteLink, Website, Page


def get_current_website(current_user_id):
    website_link = WebsiteLink.query.filter_by(user_id=current_user_id).first()
    website = Website.query.filter_by(id=website_link.website_id).first()
    return website


def get_current_website_pages(current_user_id):
    website = get_current_website(current_user_id)
    pages = Page.query.filter_by(website_id=website.id).all()
    return pages
