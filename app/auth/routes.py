from flask import render_template, flash, redirect, url_for, request

from app import db
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User

from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from flask_babel import _

from app.auth.email import send_password_reset_email
from app.auth import bp


@bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash(_("Invalid username or password"))
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc:
            next_page = url_for("main.index")
        return redirect(next_page)

    return render_template("auth/login.html", title=_("Sign in"), form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(_("Successful registration!"))
        return redirect(url_for("main.index"))

    return render_template("auth/register.html", title=_("Registration"), form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        send_password_reset_email(current_user)
        flash(_("Instructions sent to the ") + current_user.email)
        return redirect(url_for('main.user', username=current_user.username))
    else:
        form = ResetPasswordRequestForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None:
                flash(_("Wrong email!"))
                return redirect(url_for('auth.login'))
            send_password_reset_email(user)
            flash(_("Instructions sent to the ") + form.email.data)
        return render_template('auth/reset_password_request.html', form=form, title=_("Reset password"))


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_password_token(token)
    if user is None:
        return redirect(url_for('main.index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_("Password has changed"))
        return redirect(url_for('auth.login')) if not user.is_authenticated \
            else redirect(url_for('main.user', username=user.username))

    return render_template('auth/reset_password.html', title=_('Reset password'), form=form)
