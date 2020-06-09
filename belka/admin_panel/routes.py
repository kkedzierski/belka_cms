from flask import (redirect, render_template, url_for,
                   Blueprint, flash, request, g, abort)
import validators
from flask_login import login_required, current_user
from belka.models import (Website, Page, WebsiteLink, User,
                          Post)
from belka import db, bcrypt
from belka.admin_panel.utils import (is_user_website_created,
                                     create_new_empty_page,
                                     delete_page,
                                     change_page_name_in_html_file,
                                     create_directory,
                                     delete_directory,
                                     change_directory_name,
                                     create_home_page,
                                     get_current_website,
                                     is_directory_exist,
                                     get_current_website_pages,
                                     get_user_role,
                                     get_website_by_id,
                                     save_picture,
                                     UserRoles)
from belka.admin_panel.forms import (CreateUserForm, UpdateAccountForm,
                                     UpdateUserForm, PostForm)


main_panel = Blueprint('main_panel', __name__)

# region Getting Started
@main_panel.route('/getting-started')
@login_required
def getting_started():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if is_user_website_created(current_user.id):
        flash('You cannot create another website. You have one!', 'info')
        return redirect(url_for('main_panel.admin_panel'))
    return render_template('admin_panel/getting_started/getting-started.html',
                           title='Getting started')


@main_panel.route('/create-website', methods=['GET', 'POST'])
@login_required
def create_website_page():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if is_user_website_created(current_user.id):
        flash('You cannot create another website. You have one!', 'info')
        return redirect(url_for('main_panel.admin_panel'))
    return render_template('admin_panel/getting_started/create-website.html',
                           title="Create website")


@main_panel.route('/create-website/create-website', methods=['GET', 'POST'])
@login_required
def create_website():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if request.method == "POST":
        website_title = request.form.get('website_name')
        if not validators.domain(website_title):
            flash('Create correct domain adress like: example.com', 'info')
            return redirect(url_for('main_panel.create_website_page'))
        if is_directory_exist(website_title):
            flash('Website {website_name} exist '
                  'choose another name'.format(website_name=website_title),
                  'danger')
            return redirect(url_for('main_panel.create_website_page'))
        create_directory(website_title)
        create_home_page(website_title)
        website = Website(title=website_title)
        db.session.add(website)
        db.session.commit()
        website_link = WebsiteLink(website_name=website_title,
                                   website_id=website.id)
        db.session.add(website_link)
        db.session.commit()
        current_user.website_link_id = website_link.id
        db.session.commit()
        flash('You created your website, to watch your website click button'
              ' on left menu', 'success')
        return redirect(url_for('main_panel.admin_panel'))
    if is_user_website_created(current_user.id):
        flash('You cannot create another website. You have one!', 'info')
        return redirect(url_for('main_panel.admin_panel'))
# endregion

# region Styles
@main_panel.route('/hotel')
def hotel_website():
    return render_template('website_style/hotel.html', title="Hotel style")


@main_panel.route('/travel')
def travel_website():
    return render_template('website_style/travel.html', title="Travel style")


@main_panel.route('/paiting')
def paiting_website():
    return render_template('website_style/painting.html',
                           title="Paintng style")
# endregion

@main_panel.route('/admin-panel', methods=['GET', 'POST'])
@login_required
def admin_panel():
    website = get_current_website(current_user.website_link_id)
    if current_user.user_role != 1:
        role = "disabled"
        return render_template('admin_panel/admin-panel.html',
                               title="Admin Panel",
                               website=website, role=role)
    if website is None:
        return redirect(url_for('main_panel.getting_started'))
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    return render_template('admin_panel/admin-panel.html', title="Admin Panel",
                           website=website)


@main_panel.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    website = get_current_website(current_user.website_link_id)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main_panel.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',
                         filename='images/' + current_user.image_file)
    return render_template('admin_panel/account.html',
                           title='Update User', form=form,
                           website=website, image_file=image_file)

#region users
@main_panel.route('/users', methods=['GET', 'POST'])
def users_page():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    form = CreateUserForm()
    website = get_current_website(current_user.website_link_id)
    users = User.query.filter(User.user_role != 1).all()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data
                                                        ).decode('utf-8')
        user_role = get_user_role(form.user_role.data)
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password,
                    user_role=user_role,
                    website_link_id=current_user.website_link_id)
        db.session.add(user)
        db.session.commit()
        flash('Your create user: '
              '{user_name}'.format(user_name=user.username),
              'success')
        return redirect(url_for('main_panel.users_page'))
    return render_template('admin_panel/users/users.html', website=website,
                           form=form, users=users)


@main_panel.route('/users/user/operations', methods=['GET', 'POST'])
def user_operations():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    if request.form.get('user_select') is not None:
        if request.form.get('action') == "Delete user":
            username = request.form.get('user_select')
            user = User.query.filter_by(username=username).first()
            db.session.delete(user)
            db.session.commit()
            flash('The {user} has been deleted!'.format(user=username),
                  'success')
            return redirect(url_for('main_panel.users_page'))
        if request.form.get('action') == "Change user data":
            username = request.form.get('user_select')
            user = User.query.filter_by(username=username).first()
            return redirect(url_for('main_panel.change_user_data',
                                    user_id=user.id))
    else:
        flash('You need to select user', 'info')
        return redirect(url_for('main_panel.users_page'))


@main_panel.route('/users/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def change_user_data(user_id):
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    form = UpdateUserForm()
    users = User.query.filter(User.user_role != 1).all()
    user = User.query.filter_by(id=user_id).first()
    website = get_current_website(current_user.website_link_id)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.commit()
        flash('User account has been updated!', 'success')
        return redirect(url_for('main_panel.users_page'))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.password.data = user.password
    return render_template('admin_panel/users/users.html',
                           title='Update User', form=form,
                           website=website, users=users)


#endregion

#region Navigation
@main_panel.route('/apperance/navigation', methods=['GET', 'POST'])
def navigation_page():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    website = get_current_website(current_user.website_link_id)
    return render_template('admin_panel/apperance/navigation.html',
                           title="Navigation bar", website=website)


@main_panel.route('/apperance/navigation/font-size', methods=['GET', 'POST'])
def change_nav_font_size():
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    if request.method == 'POST':
        navbarFont = request.form.get('navbarFontSize')
        website = get_current_website(current_user.website_link_id)
        website.navbar_font_size = navbarFont
        db.session.commit()
        flash('Navigation font size changed', 'success')
        return redirect(url_for('website.index', website_name=website.title))


@main_panel.route('/apperance/navigation/font-family', methods=['GET', 'POST'])
def change_nav_font_family():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    if request.method == 'POST':
        navbarFontFamily = request.form.get('navbarFontFamily')
        website = get_current_website(current_user.website_link_id)
        website.navbar_font_style = navbarFontFamily
        db.session.commit()
        flash('Navigation font family changed', 'success')
        return redirect(url_for('website.index', website_name=website.title))


@main_panel.route('/apperance/navigation/styles', methods=['POST'])
def change_navigation():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    if request.method == 'POST':
        if request.form.get('nav_style') == "green":
            nav_style = "navbar-dark bg-success"
        if request.form.get('nav_style') == "dark":
            nav_style = "navbar-dark bg-dark"
        if request.form.get('nav_style') == 'blue':
            nav_style = "navbar-dark bg-info"
        website = get_current_website(current_user.website_link_id)
        website.nav_style = nav_style
        website.footer_style = nav_style
        db.session.commit()
        flash('Navigation bar changed', 'success')
        return redirect(url_for('website.index', website_name=website.title))
# endregion

#region Content
@main_panel.route('/apperance/content/content', methods=['GET', 'POST'])
def content_page():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    website = get_current_website(current_user.website_link_id)
    return render_template('admin_panel/apperance/content/content.html',
                           title="Content", website=website)


@main_panel.route('/apperance/content/font-size-page', methods=['GET', 'POST'])
def font_size_page():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    website = get_current_website(current_user.website_link_id)
    return render_template('admin_panel/apperance/content/font-size.html',
                           title="Font size", website=website)


@main_panel.route('/apperance/content/font-size', methods=['GET', 'POST'])
def change_font_size():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    if request.method == 'POST':
        website = get_current_website(current_user.website_link_id)
        title_post_font = request.form.get('titlePostFont')
        website.title_post_font_size = title_post_font
        db.session.commit()
        post_text_font = request.form.get('PostTextFont')
        website.post_text_font_size = post_text_font
        db.session.commit()
        flash('Post font size changed', 'success')
        return redirect(url_for('website.index', website_name=website.title))


@main_panel.route('/apperance/content/font-style', methods=['GET', 'POST'])
def font_style_page():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    website = get_current_website(current_user.website_link_id)
    return render_template('admin_panel/apperance/content/font-style.html',
                           title="Font style", website=website)


@main_panel.route('/apperande/content/change-post-font-style',
                  methods=['GET', 'POST'])
def change_post_font_style():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if request.method == 'POST':
        post_font_family = request.form.get('PostFontFamily')
        website = get_current_website(current_user.website_link_id)
        website.post_text_font_style = post_font_family
        website.title_post_font_style = post_font_family
        db.session.commit()
        flash('Post font family changed', 'success')
        return redirect(url_for('website.index', website_name=website.title))


@main_panel.route('/apperance/content/background-style', methods=['GET', 'POST'])
def background_page():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    website = get_current_website(current_user.website_link_id)
    return render_template('admin_panel/apperance/content/background-style.html',
                           title="Background style", website=website)

@main_panel.route('/apperance/content/background/style', methods=['GET', 'POST'])
def background_style():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    if request.method == 'POST':
        if request.form.get('backround_style') == "hotel":
            backround_style = "hotel.png"
        if request.form.get('backround_style') == "spikes":
            backround_style = "spikes.png"
        if request.form.get('backround_style') == 'painting':
            backround_style = "painting.png"
        if request.form.get('backround_style') == 'flower':
            backround_style = "flower.png"
        website = get_current_website(current_user.website_link_id)
        website.page_background = backround_style
        db.session.commit()
        flash('Background changed', 'success')
        return redirect(url_for('website.index', website_name=website.title))
# endregion

#region Pages
@main_panel.route('/pages', methods=['GET', 'POST'])
def pages():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    pages = get_current_website_pages(current_user.website_link_id)
    website = get_current_website(current_user.website_link_id)
    return render_template('admin_panel/pages/pages.html', title="pages",
                           website=website, pages=pages)


@main_panel.route('/pages/create-new-page', methods=['GET', 'POST'])
def create_new_page():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    if request.method == 'POST':
        title_page = request.form.get('page_name')
        website = get_current_website(current_user.website_link_id)
        create_new_empty_page(website.title, title_page)
        page = Page(title_page=title_page, website_id=website.id)
        db.session.add(page)
        db.session.commit()
        flash('You created new page!', 'success')
    pages = get_current_website_pages(current_user.website_link_id)
    website = get_current_website(current_user.website_link_id)
    return render_template('admin_panel/pages/pages.html',
                           pages=pages, website=website)


@main_panel.route('/pages/page/operations', methods=['GET', 'POST'])
def page_operations():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    if request.form.get('page_select') is not None:
        website = get_current_website(current_user.website_link_id)
        if request.form.get('action') == "Delete page":
            title = request.form.get('page_select')
            delete_page(title, current_user.website_link_id)
            page = Page.query.filter_by(title_page=title,
                                        website_id=website.id).first()
            db.session.delete(page)
            db.session.commit()
            flash('This page has been deleted!', 'success')
            return redirect(url_for('main_panel.pages'))
        if request.form.get('action') == "Change page name":
            title = request.form.get('page_select')
            return render_template('admin_panel/pages/change-page-name.html',
                                   title="Change page name",
                                   page_title=title, website=website)
    else:
        flash('You need to select pages', 'info')
        return redirect(url_for('main_panel.pages'))


@main_panel.route('/pages/page/change-page-name', methods=['GET', 'POST'])
def change_page_name():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    title = request.form.get('page_name')
    website = get_current_website(current_user.website_link_id)
    page = Page.query.filter_by(title_page=title,
                                website_id=website.id).first()
    page.title_page = request.form.get('new_page_name')
    change_page_name_in_html_file(title, page.title_page,
                                  current_user.id)
    db.session.commit()
    flash('Page name changed to {title}'.format(title=page.title_page),
          'success')
    return redirect(url_for('main_panel.pages'))

#endregion

#region Posts
@main_panel.route('/posts', methods=['GET', 'POST'])
def posts():
    form = PostForm()
    if current_user.user_role != 1:
        role = "disabled"
    else:
        role = ""
    if current_user.user_role == "author":
        posts = Post.query.filter_by(user_id=current_user.id).all()
    else:
        posts = Post.query.all()
    pages = get_current_website_pages(current_user.website_link_id)
    website = get_current_website(current_user.website_link_id)
    website_link = WebsiteLink.query.filter_by(website_id=website.id).first()
    if form.validate_on_submit():
        if request.form.get('page_select') is not None:
            website = get_current_website(current_user.website_link_id)
            title_page = request.form.get('page_select')
            post = Post(title=form.title.data, content=form.content.data,
                        author=current_user, post_page=title_page,
                        user_id=current_user.id,
                        website_link_id=website_link.id)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('website.index',
                            website_name=website.title))
    return render_template('admin_panel/posts/posts.html',
                           title="Posts", website=website,
                           pages=pages, form=form,
                           posts=posts, role=role)


@main_panel.route('/posts/post-operations', methods=['GET', 'POST'])
@login_required
def post_operations():
    if request.method == 'POST':
        if request.form.get('post_select') is not None:
            if request.form.get('action') == "Delete post":
                post_title = request.form.get('post_select')
                post = Post.query.filter_by(title=post_title).first()
                db.session.delete(post)
                db.session.commit()
                flash('The {post} has been deleted!'.format(post=post_title),
                      'success')
                return redirect(url_for('main_panel.posts'))
            if request.form.get('action') == "Update post":
                post_title = request.form.get('post_select')
                post = Post.query.filter_by(title=post_title).first()
                return redirect(url_for('main_panel.update_post',
                                        post_id=post.id))
        else:
            flash('You need to select post', 'info')
            return redirect(url_for('main_panel.posts'))

@main_panel.route('/posts/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    form = PostForm()
    post = Post.query.filter_by(id=post_id).first()
    website = get_current_website(current_user.website_link_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post has been updated!', 'success')
        return redirect(url_for('main_panel.posts'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('admin_panel/posts/posts.html',
                           title='Update Post', form=form,
                           website=website)
#endregion

# region Settings
@main_panel.route('/settings')
def settings_page():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    website = get_current_website(current_user.website_link_id)
    return render_template('admin_panel/settings/settings.html',
                           title="settings", website=website)


@main_panel.route('/settings/delete-website', methods=['GET', 'POST'])
def delete_website():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    website = get_current_website(current_user.website_link_id)
    website_link = WebsiteLink.query.filter_by(website_id=website.id).first()
    WebsiteLink.query.filter(WebsiteLink.id == website_link.id).delete()
    delete_directory(website.title)
    Website.query.filter(Website.id == website.id).delete()
    Page.query.filter(Page.website_id == website.id).delete()
    User.query.filter(User.website_link_id == website_link.id).delete()
    Post.query.filter(Post.website_link_id == website_link.id).delete()
    db.session.commit()
    flash('Website has been deleted', 'info')
    return redirect(url_for('main_panel.getting_started'))


@main_panel.route('/settings/change-website-name', methods=['GET', 'POST'])
def change_website_name_page():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    website = get_current_website(current_user.website_link_id)
    return render_template('admin_panel/settings/change-website-name.html',
                           title="Change website name",
                           website=website)


@main_panel.route('/settings/change/name', methods=['GET', 'POST'])
def change_website_name():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    website = get_current_website(current_user.website_link_id)
    new_website_name = request.form.get('website_name')
    if not validators.domain(new_website_name):
        flash('Create correct domain adress like: example.com', 'info')
        return redirect(url_for('main_panel.change_website_name_page'))
    change_directory_name(website.title, new_website_name)
    website.title = new_website_name
    db.session.commit()
    flash('Website name changed to {title}'.format(title=website.title),
          'success')
    return redirect(url_for('main_panel.admin_panel'))


@main_panel.route('/settings/show-admin-panel', methods=['GET', 'POST'])
def show_admin_panel():
    if current_user.user_role != 1:
        flash('You dont have access to this page', 'danger')
        return redirect(url_for('main_panel.admin_panel'))
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    website = get_current_website(current_user.website_link_id)
    if request.form.get('admin_panel_view'):
        flash('Admin panel turn on', 'success')
        website.show_admin_panel = True
        db.session.commit()
    else:
        flash('Admin panel turn off', 'success')
        website.show_admin_panel = False
        db.session.commit()
    return redirect(url_for('main_panel.settings_page'))
# endregion