from db import db


class ItemModel(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    category = db.Column(db.String())
    is_featured = db.Column(db.Boolean())
    price = db.Column(db.Float(precision=2))
    image_URL = db.Column(db.String())

    def __init__(self, name, description, category, is_featured, price, image_URL):
        self.name = name
        self.description = description
        self.category = category
        self.is_featured = is_featured
        self.price = price
        self.image_URL = image_URL

    def json_item(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'isFeatured': self.is_featured,
            'price': self.price,
            'imageUrl': self.image_URL
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_fav_id(cls, fav_item_ids):
        list = []
        for _id in fav_item_ids:
            list.append(cls.query.filter_by(id=_id).all())
        favObjs = [item for sublist in list for item in sublist]
        return favObjs

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
