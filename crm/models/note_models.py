from datetime import datetime

from sqlalchemy import ForeignKey

from crm import db
from ..models import User


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String)
    image = db.Column(db.String)
    client_id = db.Column(db.Integer, ForeignKey('client.id'))
    offer_id = db.Column(db.Integer, ForeignKey('offer.id'))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    expire_date = db.Column(db.DateTime)
    on_todo_list = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Note {self.id, self.title}>'

    @staticmethod
    def get_all():
        return Note.query.all()

    @staticmethod
    def get_all_with_users():
        return Note.query.with_entities(Note.id, Note.title, Note.description, User.initials).join(User)

    @staticmethod
    def get_by_id_with_user(idx):
        return Note.query.with_entities(Note.id, Note.title, Note.description, Note.image, Note.expire_date, User.initials) \
            .filter_by(id=idx)\
            .join(User).one()

    @staticmethod
    def get_by_offer_id(offer_id):
        return Note.query.filter_by(offer_id=offer_id).all()

    @staticmethod
    def get_by_user_id(user_id):
        return Note.query.filter_by(user_id=user_id).all()

    # @staticmethod
    # def get_by_unique_constrain(year, offer_number, offer_version):
    #     return Offer.query.filter_by(year=year, offer_number=offer_number, offer_version=offer_version).first()
    #
    # @staticmethod
    # def get_all_with_users_initials():
    #     return Offer.query.with_entities(
    #         Offer.id,
    #         Offer.year,
    #         Offer.offer_number,
    #         Offer.offer_version,
    #         User.initials,
    #         Client.name,
    #         Client.surname
    #     ).join(User, Client)
