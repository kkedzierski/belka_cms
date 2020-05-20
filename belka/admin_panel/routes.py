from flask import (redirect, render_template, url_for,
                   Blueprint, flash, request)
from flask_login import login_user, logout_user, current_user, login_required
from belka.admin_panel.forms import RegistrationForm, LoginForm
from belka.models import User
from belka import bcrypt, db

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        print("Your validate is great!")
        hashed_password = bcrypt.generate_password_hash(form.password.data
                                                        ).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!, You can log in',
              'success')
        return redirect(url_for('main.sign_in'))
    return render_template("sign_in/sign_up.html", title='Register', form=form)


@main.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have logged in successful!', 'success')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.getting_start'))
        else:
            flash('Login Unsuccessful. Please check your email and passoword',
                  'danger')
    return render_template("sign_in/sign_in.html", title='Login', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout Successful!', 'success')
    return redirect(url_for('main.sign_up'))


@main.route('/getting-start')
def getting_start():
    return render_template('admin_panel/getting-start.html',
                           title='Getting started')


@main.route('/create-website')
def create_website():
    return render_template('admin_panel/create-website.html',
                           title="Create website")


@main.route('/hotel')
def hotel_website():
    return render_template('website_style/hotel.html', title="Hotel style")


@main.route('/index')
def index():
    return render_template('main_website/index.html', title="Your website")
