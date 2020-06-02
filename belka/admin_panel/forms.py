from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField,
                     SubmitField, BooleanField, RadioField)
from wtforms.validators import (DataRequired, Length, Email,
                                EqualTo, ValidationError)
from belka.models import User


class CreateUserForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder": "Login"})
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')],
                                     render_kw={"placeholder":
                                                "Confirm password"})
    user_role = RadioField('Role', choices=[('1', 'Admin'),
                                            ('2', 'Editor'),
                                            ('3', 'Author')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This name is already taken,"
                                  "choose another name")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Account with this email exist"
                                  "choose another email")

