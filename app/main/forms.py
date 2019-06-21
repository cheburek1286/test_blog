from flask_wtf import FlaskForm

from wtforms import fields, validators, ValidationError
from flask_wtf.file import FileField, FileAllowed

from app.models import User

from flask_babel import lazy_gettext as _l
from flask_babel import _

from flask import request


class EditProfileForm(FlaskForm):
    username = fields.StringField(_("username"), validators=[validators.DataRequired()])
    avatar = FileField("image", validators=[FileAllowed(['jpg', 'png', 'jpeg'], _('Images only!'))])
    submit = fields.SubmitField(_("save"))

    def __init__(self, name, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.name = name

    def validate_username(self, username):
        if self.name != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(_('Duplicate username'))


class PostForm(FlaskForm):
    post = fields.TextAreaField(_l('Your post'), validators=[validators.DataRequired(), validators.Length(max=200)])
    submit = fields.SubmitField(_l('Post'))


class SearchForm(FlaskForm):
    q = fields.StringField(_l('Search'), validators=[validators.DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False

        super(SearchForm, self).__init__(*args, **kwargs)



