from belka import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    user_role = db.Column(db.Integer)
    websiteLink_id = db.Column(db.ForeignKey('websitelink.id'),
                               nullable=True)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return "User({username},"\
               "{email},"\
               "{image_file})".format(username=self.username,
                                      email=self.email,
                                      image_file=self.image_file)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    post_page = db.Column(db.String, nullable=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Post({title},"\
               "{date_posted}".format(title=self.title,
                                      date_posted=self.date_posted)


class WebsiteLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website_name = db.Column(db.String, nullable=False)
    website_id = db.Column(db.ForeignKey('website.id'), nullable=False)
    users = db.relationship('User', backref='author', lazy=True)

    def __repr__(self):
        return "WebsiteLink({website_name},"\
               "WebisteLink id = {id},"\
               "website_id= {website_id},"\
               "".format(website_name=self.website_name,
                         id=self.id,
                         website_id=self.website_id)


class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    nav_style = db.Column(db.String(200), nullable=True)
    page_background = db.Column(db.String(200), nullable=True)
    navbar_font_style = db.Column(db.String(200), nullable=True)
    title_post_font_style = db.Column(db.String(200), nullable=True)
    post_text_font_style = db.Column(db.String(200), nullable=True)
    navbar_font_size = db.Column(db.String(200), nullable=True)
    title_post_font_size = db.Column(db.String(200), nullable=True)
    post_text_font_size = db.Column(db.String(200), nullable=True)
    footer_style = db.Column(db.String(200), nullable=True)
    show_admin_panel = db.Column(db.Boolean(), nullable=False,
                                 default=True)

    def __repr__(self):
        return "Website({title})".format(title=self.title)


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_page = db.Column(db.String(200))
    website_id = db.Column(db.ForeignKey('website.id'), nullable=False)

    def __repr__(self):
        return "Page({title}, "\
               "website_id = {website_id})".format(title=self.title_page,
                                                   website_id=self.website_id)
