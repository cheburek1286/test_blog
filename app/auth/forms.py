from flask_wtf import FlaskForm

from wtforms import fields, validators, ValidationError

from app.models import User

from flask_babel import lazy_gettext as _l
from flask_babel import _

import re


# def password_validators(password):
#
#     if len(password.data) < 6:
#         raise ValidationError('Password length is less than 6 characters')
#
#     if not re.search("(?=.*[0-9])", password.data):
#         raise ValidationError('Password should contain digits 0-9')
#
#     if not re.search("(?=.*[a-z])", password.data):
#         raise ValidationError('Password should contain lowercase characters')
#
#     if not re.search("(?=.*[A-Z])", password.data):
#         raise ValidationError('Password should contain uppercase characters')
#
#     if not re.search("(?=.*[!@#$%])", password.data):
#         raise ValidationError('Password should contain !@#$%')


class LoginForm(FlaskForm):
    username = fields.StringField(_l("username"), validators=[validators.DataRequired()])
    password = fields.PasswordField(_l("password"), validators=[validators.DataRequired()])
    remember_me = fields.BooleanField(_l("remember me"))
    submit = fields.SubmitField(_l("sign in"))


class RegistrationForm(FlaskForm):
    username = fields.StringField(_l("username"), validators=[validators.DataRequired()])
    email = fields.StringField(_l("email"), validators=[validators.DataRequired(), validators.Email()])
    password = fields.PasswordField(_l("password"), validators=[validators.DataRequired()])
    repeat_password = fields.PasswordField(_l("repeat password"),
                                           validators=[
                                               validators.DataRequired(),
                                               validators.EqualTo("password", message=_l("Passwords don't match"))
                                           ])
    submit = fields.SubmitField(_l("register"))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(_l('Duplicate username'))

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(_l('Duplicate email'))


class ResetPasswordRequestForm(FlaskForm):
    email = fields.StringField(_l('Email'), validators=[validators.DataRequired(), validators.Email()])
    submit = fields.SubmitField(_l('Reset password'))


class ResetPasswordForm(FlaskForm):
    password = fields.PasswordField(_('password'), validators=[validators.DataRequired()])
    repeat_password = fields.PasswordField(_("repeat password"),
                                           validators=[
                                               validators.DataRequired(),
                                               validators.EqualTo("password", message=_l("Passwords don't match"))
                                           ])
    submit = fields.SubmitField(_("reset password"))