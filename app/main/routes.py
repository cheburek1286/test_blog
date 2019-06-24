from flask import render_template, flash, redirect, url_for, request, send_from_directory, jsonify, current_app

from app import db
from app.main.forms import EditProfileForm, PostForm, SearchForm
from app.models import User, Post

from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from flask_babel import _

from flask import g
from flask_babel import get_locale

from guess_language import guess_language
from app.translate import translate

from datetime import datetime

import os

from app.main import bp


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        if current_app.elasticsearch:
            g.search_form = SearchForm()

    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    form = PostForm()
    if form.validate_on_submit():
        lang = guess_language(form.post.data)
        if lang == 'UNKNOWN' or len(lang) > 5:
            lang = ""

        post = Post(author=current_user, body=form.post.data, language=lang)
        db.session.add(post)
        db.session.commit()
        flash(_("Your post was saved"))
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, current_app.config["POST_PER_PAGE"], False)

    next = url_for('main.index', page=posts.next_num) if posts.has_next else None
    prev = url_for('main.index', page=posts.prev_num) if posts.has_prev else None

    return render_template("index.html", title=_("Sychevalnya"), posts=posts.items, form=form, prev_url=prev, next_url=next)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(user_id=user.id).order_by(
        Post.timestamp.desc()).paginate(page, current_app.config['POST_PER_PAGE'], False)

    next = url_for('main.user', username=username, page=posts.next_num) if posts.has_next else None
    prev = url_for('main.user', username=username, page=posts.prev_num) if posts.has_prev else None

    return render_template("user.html", title=_("User profile"),
                           posts=posts.items, user=user, next_url=next, prev_url=prev)


@bp.route('/edit_profile', methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():

        file = form.avatar.data
        if file is not None:
            last_avatar_filename = current_user.avatar_filename
            if last_avatar_filename and os.path.exists(current_app.config["IMG_FOLDER"] + "/" + last_avatar_filename):
                os.remove(current_app.config["IMG_FOLDER"] + "/" + last_avatar_filename)

            user_filename = secure_filename(file.filename)
            ext = user_filename.split('.')[-1]
            storage_filename = 'avatar_' + str(current_user.id) + '.' + ext
            save_dir = current_app.config["IMG_FOLDER"] + "/" + storage_filename
            file.save(save_dir)
            current_user.avatar_filename = storage_filename

        current_user.username = form.username.data

        db.session.commit()
        flash(_("Changed saved"))
        return redirect(url_for("main.edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username

    return render_template("edit_profile.html", form=form, title=_("Edit profile"))


@bp.route('/static/img/<filename>')
@login_required
def send_img(filename):
    return send_from_directory(current_app.config["IMG_FOLDER"], filename)


@bp.route('/static/<filename>')
@login_required
def send_file(filename):
    return send_from_directory(current_app.config["STATIC_FOLDER"], filename)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash(_("Bad username!"))
        return redirect(url_for("index"))

    current_user.follow(user)
    db.session.commit()
    flash(_("You're following ") + user.username)
    return redirect(url_for("main.user", username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash(_("Bad username!"))
        return redirect(url_for("main.index"))

    current_user.unfollow(user)
    db.session.commit()
    flash(_("You're not following ") + user.username + _(" anymore"))
    return redirect(url_for("main.user", username=username))


@bp.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users, group=_("Users"), title=_('All users'))


@bp.route('/followers/<username>')
@login_required
def followers(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash(_("Bad username!"))
        return redirect(url_for("main.index"))

    group_name = _("Your followers") if current_user.username == username else username + _("'s followers")

    users = user.followers.all()
    return render_template('users.html', users=users, group=group_name, title=_('Followers'))


@bp.route('/followed/<username>')
@login_required
def followed(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash(_("Bad username!"))
        return redirect(url_for("main.index"))

    group_name = _("Your are followed") if current_user.username == username else username + _("'s followed")

    users = user.followed.all()
    return render_template('users.html', users=users, group=group_name, title=_('Followed'))


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify(
        {
            "text": translate(request.form['text'], request.form['source_language'], request.form['dest_language'])
        }
    )


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.index'))

    posts_per_page = current_app.config["POST_PER_PAGE"]

    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page, posts_per_page)

    next_url = url_for('main.search', q=g.search_form.data, page=page + 1) if total > page * posts_per_page else None
    prev_url = url_for('main.search', q=g.search_form.data, page=page - 1) if page > 1 else None

    return render_template('search.html', title=_('Search'), posts=posts, next_url=next_url, prev_url=prev_url)

