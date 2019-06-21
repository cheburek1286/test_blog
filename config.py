import os

root_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = "dkebgkjbssghdzhbkbkhrt68mgdmAfhDZGEev1uyg"

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(root_dir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    IMG_FOLDER = os.path.join(root_dir, 'static/img')
    STATIC_FOLDER = os.path.join(root_dir, 'static')

    POST_PER_PAGE = 10

    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = "LeraVostrikova94@gmail.com"
    MAIL_PASSWORD = "a459k13tgm"
    ADMINS = ["LeraVostrikova94@gmail.com"]

    LANGUAGES = ['en', 'ru']
    MS_TRANSLATOR_KEY = "trnsl.1.1.20190618T091041Z.35db3c610d1d72cc.ffc7cc3c9a40b1a55b79ee344d06a4bc46014ee7"

    ELASTICSEARCH_URL = None #"http://127.0.0.1:9200"