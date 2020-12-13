from crm import db


class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    offer_number = db.Column(db.Integer, nullable=False, unique=True)

    def __repr__(self):
        return '<Offer %r' % self.offer_number

    @staticmethod
    def get_all():
        return Offer.query.all()
