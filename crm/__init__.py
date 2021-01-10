import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists


from .settings import Settings
db = SQLAlchemy()

login_manager = LoginManager()


def create_app():
    crm_app = Flask(__name__)

    from .main import bp_main
    from .user import bp_user
    from .auth import bp_auth
    from .client import bp_client
    from .offer import bp_offer
    from .note import bp_note
    from .settings import bp_settings

    crm_app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(Settings.get_instance().settings['STANDARD_FOLDER_PATH'], 'crm.db')}"
    crm_app.config['SECRET_KEY'] = b'\x1aB\xd6\x15\x98\x9ebfk\xfd\xb1b\x06\x0fQ\x81\x0c\x07\xfe&\xc1\x84\x9dU'

    crm_app.register_blueprint(bp_main, url_prefix='/')
    crm_app.register_blueprint(bp_user, url_prefix='/user')
    crm_app.register_blueprint(bp_auth, url_prefix='/auth')
    crm_app.register_blueprint(bp_client, url_prefix='/client')
    crm_app.register_blueprint(bp_offer, url_prefix='/offer')
    crm_app.register_blueprint(bp_note, url_prefix='/note')
    crm_app.register_blueprint(bp_settings, url_prefix='/settings')

    db.init_app(crm_app)

    if database_exists(crm_app.config['SQLALCHEMY_DATABASE_URI']) is False:
        with crm_app.app_context():
            db.create_all()

    Migrate(crm_app, db)

    login_manager.init_app(crm_app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'

    return crm_app
