from db import db
import datetime


class OrderModel(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    confirmation_num = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total = db.Column(db.Float(precision=2))
    user = db.relationship('UserModel')

    def __init__(self, confirmation_num, user_id, total):
        self.confirmation_num = confirmation_num
        self.user_id = user_id
        self.total = total

    def json(self):
        return {'id': self.id, 'confirmationNum': self.confirmation_num, 'userId': self.user_id, 'total': self.total}

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
