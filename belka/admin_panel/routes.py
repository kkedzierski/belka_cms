from flask import (redirect, render_template, url_for,
                   Blueprint, flash, request)


main_panel = Blueprint('main_panel', __name__)


@main_panel.route('/getting-start')
def getting_start():
    return render_template('admin_panel/getting-start.html',
                           title='Getting started')


@main_panel.route('/create-website')
def create_website():
    return render_template('admin_panel/create-website.html',
                           title="Create website")


@main_panel.route('/hotel')
def hotel_website():
    return render_template('website_style/hotel.html', title="Hotel style")


@main_panel.route('/admin-panel')
def admin_panel():
    return render_template('admin_panel/admin-panel.html', title="Admin Panel")
