from flask import (redirect, render_template, url_for,
                   Blueprint, flash, request)
from flask_login import login_user, logout_user, current_user, login_required
from belka.authentication_panel.forms import RegistrationForm, LoginForm
from belka.models import User, Website
from belka import bcrypt, db
from belka.authentication_panel.utils import (is_user_website_created,
                                              UserRoles)


authentication = Blueprint('authentication', __name__)


@authentication.route('/', methods=['GET', 'POST'])
@authentication.route('/sign_up', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if is_user_website_created(current_user.id):
            return redirect(url_for('main_panel.admin_panel'))
        else:
            return redirect(url_for('main_panel.getting_started'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data
                                                        ).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password,
                    user_role=UserRoles.admin.value)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!, You can log in',
              'success')
        return redirect(url_for('authentication.login'))
    return render_template("authentication_panel/register.html",
                           title='Register', form=form)


@authentication.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if is_user_website_created(current_user.id):
            return redirect(url_for('main_panel.admin_panel'))
        else:
            return redirect(url_for('main_panel.getting_started'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            # next_page = request.args.get('next')
            flash('You have logged in successful!', 'success')
            # if next_page:
            #     return redirect(next_page)
            # else:
            if is_user_website_created(current_user.id):
                return redirect(url_for('main_panel.admin_panel'))
            else:
                return redirect(url_for('main_panel.getting_started'))
        else:
            flash('Login Unsuccessful. Please check your email and passoword',
                  'danger')
    return render_template("authentication_panel/login.html",
                           title='Login', form=form)


@authentication.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout Successful!', 'success')
    return redirect(url_for('authentication.register'))
