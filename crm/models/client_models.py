from sqlalchemy import UniqueConstraint, CheckConstraint

from crm import db


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    company = db.Column(db.String(256))
    address_street_and_number = db.Column(db.String(128))
    address_zipcode_and_city = db.Column(db.String(128))
    phone = db.Column(db.String(128))
    email = db.Column(db.String(128))
    __table_args__ = (UniqueConstraint('name', 'surname', 'phone', 'email'),
                      CheckConstraint("surname <> '' OR phone  <> '' OR  email <> ''"))

    def __repr__(self):
        return '<Client %r>' % self.name

    @staticmethod
    def get_all():
        return Client.query.all()

    @staticmethod
    def get_by_id(idx):
        return Client.query.get(idx)

    @staticmethod
    def get_by_unique_constrain(name, surname, phone, email):
        return Client.query.filter_by(name=name, surname=surname, phone=phone, email=email).first()
