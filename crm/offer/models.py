from sqlalchemy import UniqueConstraint, ForeignKey

from crm import db
from ..client import Client
from ..user import User


class Offer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    offer_number = db.Column(db.Integer, nullable=False)
    offer_version = db.Column(db.String(1), nullable=False)
    client_id = db.Column(db.Integer, ForeignKey('client.id'))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))

    __table_args__ = (UniqueConstraint('year', 'offer_number', 'offer_version'),)

    def __repr__(self):
        return f'<Offer {self.offer_number, self.offer_version}>'

    @staticmethod
    def get_all():
        return Offer.query.all()

    @staticmethod
    def get_by_id(idx):
        return Offer.query.get(idx)

    @staticmethod
    def get_by_offer_number(offer_number):
        return Offer.query.filter_by(offer_number=offer_number).first()

    @staticmethod
    def get_by_unique_constrain(year, offer_number, offer_version):
        return Offer.query.filter_by(year=year, offer_number=offer_number, offer_version=offer_version).first()

    @staticmethod
    def get_all_with_user_and_client():
        return Offer.query.with_entities(
            Offer.id,
            Offer.year,
            Offer.offer_number,
            Offer.offer_version,
            User.initials,
            Client.name,
            Client.surname
        ).join(User, Client)

    @staticmethod
    def get_all_with_client_by_user(user_id):
        return Offer.query.with_entities(
            Offer.id,
            Offer.year,
            Offer.offer_number,
            Offer.offer_version,
            Client.name,
            Client.surname,
            Client.address_street_and_number,
            Client.address_zipcode_and_city
        ).filter_by(user_id=user_id).join(User, Client)
