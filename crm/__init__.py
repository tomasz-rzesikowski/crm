import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists

from .utils import Settings

db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    crm_app = Flask(__name__)

    from . import views

    crm_app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(Settings.get_instance().settings['STANDARD_FOLDER_PATH'], 'crm.db')}"
    crm_app.config['SECRET_KEY'] = b'\x1aB\xd6\x15\x98\x9ebfk\xfd\xb1b\x06\x0fQ\x81\x0c\x07\xfe&\xc1\x84\x9dU'

    crm_app.register_blueprint(views.bp_main)
    crm_app.register_blueprint(views.bp_user)
    crm_app.register_blueprint(views.bp_client)
    crm_app.register_blueprint(views.bp_offer)
    crm_app.register_blueprint(views.bp_settings)

    db.init_app(crm_app)

    if database_exists(crm_app.config['SQLALCHEMY_DATABASE_URI']) is False:
        with crm_app.app_context():
            db.create_all()

    Migrate(crm_app, db)

    return crm_app
