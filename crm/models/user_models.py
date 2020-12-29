from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from crm import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    surname = db.Column(db.String(128), nullable=False)
    initials = db.Column(db.String(128), unique=True, nullable=True)
    phone = db.Column(db.String(128), nullable=True)
    email = db.Column(db.String(128), unique=True, nullable=True)
    password_hash = db.Column(db.String)

    @property
    def password(self):
        return AttributeError('Password: write only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(idx):
        return User.query.get(idx)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_initials(initials):
        return User.query.filter_by(initials=initials).first()

    @staticmethod
    def get_all_initials():
        return User.query.with_entities(User.id, User.initials).all()
