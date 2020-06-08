from belka.models import WebsiteLink, Website, Page


def get_current_website(website_link_id):
    website_link = WebsiteLink.query.filter_by(id=website_link_id).first()
    if website_link is not None:
        website = Website.query.filter_by(id=website_link.website_id).first()
        return website
    else:
        return None


def get_current_website_pages(website_link_id):
    website = get_current_website(website_link_id)
    pages = Page.query.filter_by(website_id=website.id).all()
    return pages
