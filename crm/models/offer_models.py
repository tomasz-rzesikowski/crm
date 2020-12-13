from sqlalchemy import UniqueConstraint

from crm import db


class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    offer_number = db.Column(db.Integer, nullable=False)
    offer_version = db.Column(db.String(1), nullable=False)
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
