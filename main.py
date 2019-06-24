from app import db, create_app
from app.models import User, Post
from flask import current_app

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

import os


def run_logging_mail():
    if not current_app.debug:
        if current_app.config['MAIL_SERVER']:
            auth = None
            if current_app.config['MAIL_USERNAME'] and current_app.config['MAIL_PASSWORD']:
                auth = (current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])

            secure = None
            if current_app.config["MAIL_USE_TLS"]:
                secure = ()

            mail_handler = SMTPHandler(
                mailhost=(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']),
                fromaddr='no-reply@' + current_app.config['MAIL_SERVER'],
                toaddrs=current_app.config['ADMINS'], subject='Shit happens...',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            current_app.logger.addHandler(mail_handler)


def run_logging_file():

    if not current_app.debug:

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        current_app.logger.addHandler(file_handler)

        current_app.logger.setLevel(logging.INFO)
        current_app.logger.info('microblog info')


def db_clear():

    for user in User.query.all():
        db.session.delete(user)
    db.session.commit()

    for post in Post.query.all():
        db.session.delete(post)

    db.session.commit()


app = create_app()

# run_logging_mail()
# run_logging_file()

app.run(host="127.0.0.1", port=int("1000"))
