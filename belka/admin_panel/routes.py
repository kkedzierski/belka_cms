from flask import (redirect, render_template, url_for,
                   Blueprint, flash, request, g, abort)
from flask_login import login_required, current_user
from belka.models import Website, Page, WebsiteLink
from belka import db
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
                                     get_current_website_pages)
from belka.admin_panel.forms import CreateUserForm


main_panel = Blueprint('main_panel', __name__)

# region Getting Started
@main_panel.route('/getting-started')
@login_required
def getting_started():
    if is_user_website_created(current_user.id):
        flash('You cannot create another website. You have one!', 'info')
        return redirect(url_for('main_panel.admin_panel'))
    return render_template('admin_panel/getting_started/getting-started.html',
                           title='Getting started')


@main_panel.route('/create-website', methods=['GET', 'POST'])
@login_required
def create_website_page():
    if is_user_website_created(current_user.id):
        flash('You cannot create another website. You have one!', 'info')
        return redirect(url_for('main_panel.admin_panel'))
    return render_template('admin_panel/getting_started/create-website.html',
                           title="Create website")


@main_panel.route('/create-website/create-website', methods=['GET', 'POST'])
@login_required
def create_website():
    if request.method == "POST":
        website_title = request.form.get('website_name')
        if is_directory_exist(website_title):
            flash('Website {website_name} exist '
                  'choose another name'.format(website_name=website_title), 'danger')
            return redirect(url_for('main_panel.create_website_page'))
        create_directory(website_title)
        create_home_page(website_title)
        g.user = current_user.get_id()
        website = Website(title=website_title)
        db.session.add(website)
        db.session.commit()
        website_link = WebsiteLink(website_name=website_title,
                                   user_id=g.user,
                                   website_id=website.id)
        db.session.add(website_link)
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
    website = get_current_website(current_user.id)
    if website is None:
        return redirect(url_for('main_panel.getting_started'))
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    return render_template('admin_panel/admin-panel.html', title="Admin Panel",
                           website=website)

#region users
@main_panel.route('/users', methods=['GET', 'POST'])
def users_page():
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    form = CreateUserForm()
    website = get_current_website(current_user.id)
    return render_template('admin_panel/users.html', website=website,
                           form=form)
#endregion

#region Navigation
@main_panel.route('/apperance/navigation', methods=['GET', 'POST'])
def navigation_page():
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    website = get_current_website(current_user.id)
    return render_template('admin_panel/apperance/navigation.html',
                           title="Navigation bar", website=website)


@main_panel.route('/apperance/navigation/font-size', methods=['GET', 'POST'])
def change_nav_font_size():
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    if request.method == 'POST':
        navbarFont = request.form.get('navbarFontSize')
        website = get_current_website(current_user.id)
        website.navbar_font_size = navbarFont
        db.session.commit()
        flash('Navigation font size changed', 'success')
        return redirect(url_for('website.index', website_name=website.title))


@main_panel.route('/apperance/navigation/font-family', methods=['GET', 'POST'])
def change_nav_font_family():
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    if request.method == 'POST':
        navbarFontFamily = request.form.get('navbarFontFamily')
        website = get_current_website(current_user.id)
        website.navbar_font_style = navbarFontFamily
        db.session.commit()
        flash('Navigation font family changed', 'success')
        return redirect(url_for('website.index', website_name=website.title))


@main_panel.route('/apperance/navigation/styles', methods=['POST'])
def change_navigation():
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
        website = get_current_website(current_user.id)
        website.nav_style = nav_style
        db.session.commit()
        flash('Navigation bar changed', 'success')
        return redirect(url_for('website.index', website_name=website.title))
# endregion

#region Content
@main_panel.route('/apperance/content/content', methods=['GET', 'POST'])
def content_page():
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    website = get_current_website(current_user.id)
    return render_template('admin_panel/apperance/content/content.html',
                           title="Content", website=website)


@main_panel.route('/apperance/content/font-size', methods=['GET', 'POST'])
def font_size_page():
    website = get_current_website(current_user.id)
    return render_template('admin_panel/apperance/content/font-size.html',
                           title="Font size", website=website)


@main_panel.route('/apperance/content/font-size', methods=['GET', 'POST'])
def change_font_size():
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    if request.method == 'POST':
        navbarFont = request.form.get('navbarFontSize')
        website = get_current_website(current_user.id)
        website.navbar_font_size = navbarFont
        db.session.commit()
        flash('Navigation font size changed', 'success')
        return redirect(url_for('website.index'))


@main_panel.route('/apperance/content/font-style', methods=['GET', 'POST'])
def font_style_page():
    website = get_current_website(current_user.id)
    return render_template('admin_panel/apperance/content/font-style.html',
                           title="Font style", website=website)


@main_panel.route('/apperance/content/background-style', methods=['GET', 'POST'])
def background_page():
    website = get_current_website(current_user.id)
    return render_template('admin_panel/apperance/content/background-style.html',
                           title="Background style", website=website)

@main_panel.route('/apperance/content/background/style', methods=['GET', 'POST'])
def background_style():
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
        website = get_current_website(current_user.id)
        website.page_background = backround_style
        db.session.commit()
        flash('Background changed', 'success')
        return redirect(url_for('website.index', website_name=website.title))
# endregion

#region Pages
@main_panel.route('/pages', methods=['GET', 'POST'])
def pages():
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    pages = get_current_website_pages(current_user.id)
    website = get_current_website(current_user.id)
    return render_template('admin_panel/pages/pages.html', title="pages",
                           website=website, pages=pages)


@main_panel.route('/pages/create-new-page', methods=['GET', 'POST'])
def create_new_page():
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    if request.method == 'POST':
        title_page = request.form.get('page_name')
        website = get_current_website(current_user.id)
        create_new_empty_page(website.title, title_page)
        page = Page(title_page=title_page, website_id=website.id)
        db.session.add(page)
        db.session.commit()
        flash('You created new page!', 'success')
    pages = get_current_website_pages(current_user.id)
    website = get_current_website(current_user.id)
    return render_template('admin_panel/pages/pages.html',
                           pages=pages, website=website)


@main_panel.route('/pages/page/operations', methods=['GET', 'POST'])
def page_operations():
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    if request.form.get('page_select') is not None:
        website = get_current_website(current_user.id)
        if request.form.get('action') == "Delete page":
            title = request.form.get('page_select')
            delete_page(title, current_user.id)
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
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    title = request.form.get('page_name')
    website = get_current_website(current_user.id)
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

# region Settings
@main_panel.route('/settings')
def settings_page():
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    website = get_current_website(current_user.id)
    return render_template('admin_panel/settings.html',
                           title="settings", website=website)


@main_panel.route('/settings/delete-website', methods=['GET', 'POST'])
def delete_website():
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    website = get_current_website(current_user.id)
    website_link = WebsiteLink.query.filter_by(website_id=website.id).first()
    WebsiteLink.query.filter(WebsiteLink.id == website_link.id).delete()
    delete_directory(website.title)
    Website.query.filter(Website.id == website.id).delete()
    db.session.query(Page).delete()
    db.session.commit()
    flash('Website has been deleted', 'info')
    return redirect(url_for('main_panel.getting_started'))


@main_panel.route('/settings/change-website-name', methods=['GET', 'POST'])
def change_website_name_page():
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    website = get_current_website(current_user.id)
    return render_template('admin_panel/change-website-name.html',
                           title="Change website name",
                           website=website)


@main_panel.route('/settings/change/name', methods=['GET', 'POST'])
def change_website_name():
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    website = get_current_website(current_user.id)
    new_website_name = request.form.get('website_name')
    change_directory_name(website.title, new_website_name)
    website.title = new_website_name
    db.session.commit()
    flash('Website name changed to {title}'.format(title=website.title),
          'success')
    return redirect(url_for('main_panel.admin_panel'))


@main_panel.route('/settings/show-admin-panel', methods=['GET', 'POST'])
def show_admin_panel():
    if not is_user_website_created(current_user.id):
        flash('You dont have a website. Create a website first!', 'info')
        return redirect(url_for('main_panel.getting_started'))
    website = get_current_website(current_user.id)
    if request.form.get('admin_panel_view'):
        print(request.form.get('admin_panel_view'))
        flash('Admin panel turn on', 'success')
        website.show_admin_panel = True
        db.session.commit()
    else:
        flash('Admin panel turn off', 'success')
        website.show_admin_panel = False
        db.session.commit()
    return redirect(url_for('main_panel.settings_page'))
# endregion