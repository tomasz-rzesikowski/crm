from crm import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    surname = db.Column(db.String(128), nullable=False)
    initials = db.Column(db.String(128), unique=True, nullable=True)
    phone = db.Column(db.String(128), nullable=True)
    email = db.Column(db.String(128), unique=True, nullable=True)

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
