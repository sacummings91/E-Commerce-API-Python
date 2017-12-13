from db import db


class OrderItemModel(db.Model):
    __tablename__ = 'order_item'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    order = db.relationship('OrderModel')
    item = db.relationship('ItemModel')

    def __init__(self, order_id, item_id):
        self.order_id = order_id
        self. item_id = item_id

    def json(self):
        return {'id': self.id, 'order_id': self.order_id, 'item_id': self.item_id}

    @classmethod
    def find_by_order_id(cls, order_id):
        return cls.query.filter_by(order_id=order_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
