from flask import (redirect, render_template, url_for,
                   Blueprint, flash, request)
from belka.models import Website
from belka import db


main_panel = Blueprint('main_panel', __name__)

# region Getting Started
@main_panel.route('/getting-started')
def getting_started():
    return render_template('admin_panel/getting_started/getting-started.html',
                           title='Getting started')


@main_panel.route('/create-website', methods=['GET', 'POST'])
def create_website_page():
    return render_template('admin_panel/getting_started/create-website.html',
                           title="Create website")


@main_panel.route('/create-website/create-website', methods=['GET', 'POST'])
def create_website():
    if request.method == "POST":
        website_name = request.form.get('website_name')
        website = Website(title=website_name)
        db.session.add(website)
        db.session.commit()
        flash('You created your website, to watch your website click button'
              ' on left menu', 'success')
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
def admin_panel():
    return render_template('admin_panel/admin-panel.html', title="Admin Panel")


@main_panel.route('/apperance/navigation', methods=['GET', 'POST'])
def navigation_page():
    return render_template('admin_panel/apperance/navigation.html',
                           title="Navigation bar")


@main_panel.route('/apperance/navigation/styles', methods=['POST'])
def change_navigation():
    if request.method == 'POST':
        if request.form.get('nav_style') == "green":
            nav_style = "navbar-dark bg-success"
        if request.form.get('nav_style') == "dark":
            nav_style = "navbar-dark bg-dark"
        if request.form.get('nav_style') == 'blue':
            nav_style = "navbar-dark bg-info"
        website = Website.query.get(1)
        website.nav_style = nav_style
        db.session.commit()
        flash('Navigation bar changed', 'success')
        return redirect(url_for('website.index'))


@main_panel.route('/settings')
def settings_page():
    return render_template('admin_panel/settings.html',
                           title="settings")


@main_panel.route('/settings/delete-website', methods=['GET', 'POST'])
def delete_website():
    db.session.query(Website).delete()
    db.session.commit()
    flash('Website has been deleted', 'info')
    return redirect(url_for('main_panel.getting_started'))


@main_panel.route('/settings/change-website-name', methods=['GET', 'POST'])
def change_website_name_page():
    website = Website.query.all()
    return render_template('admin_panel/change-website-name.html',
                           title="Change website name",
                           website=website)


@main_panel.route('/change-website-name', methods=['GET', 'POST'])
def change_website_name():
    website = Website.query.get(1)
    website.title = request.form.get('website_name')
    db.session.commit()
    flash('Website name changed to {title}'.format(title=website.title),
          'success')
    return redirect(url_for('main_panel.admin_panel'))
