from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.order_item import OrderItemModel


class OrderItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('order_id', type=int, required=True)
    parser.add_argument('item_id', type=int, required=True)

    @jwt_required()
    def get(self, order_id):
        return list(map(lambda x: x.json(), OrderItemModel.find_by_order_id(order_id)))

    @jwt_required()
    def post(self, order_id):
        data = OrderItem.parser.parse_args()

        order_item = OrderItemModel(**data)

        try:
            order_item.save_to_db()
        except:
            return {'message': 'An error ocurred inserting the order'}, 500

        return order_item.json(), 201
