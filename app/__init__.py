from flask import Flask, request, current_app

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_babel import Babel

from flask_babel import lazy_gettext as _l

from elasticsearch import Elasticsearch

from redis import Redis
import rq

from config import Config


db = SQLAlchemy()
migrate = Migrate()

login = LoginManager()
login.login_view = "auth.login"
login.login_message = _l("Please log in to access this page.")

mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None

    app.redis = Redis.from_url(app.config['REDIS_URL']) if app.config['REDIS_URL'] else None
    app.task_queue = rq.Queue('blog-tasks', connection=app.redis) if app.config['REDIS_URL'] else None

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from app import models
