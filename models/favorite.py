from db import db


class FavoriteModel(db.Model):
    __tablename__ = 'favorite'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    user = db.relationship('UserModel')
    item = db.relationship('ItemModel')

    def __init__(self, user_id, item_id):
        self.user_id = user_id
        self.item_id = item_id

    def json_favorite(self):
        return {'id': self.id, 'userId': self.user_id, 'itemId': self.item_id}

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
