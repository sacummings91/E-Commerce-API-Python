from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.order import OrderModel
from models.order_item import OrderItemModel
import logging


class Order(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('confirmation_num', type=float, required=True)
    parser.add_argument('user_id', type=int, required=True)
    parser.add_argument('total', type=float, required=True)
    parser.add_argument('item_ids', type=int, action='append', required=True)

    @jwt_required()
    def get(self, _id):
        order = OrderModel.find_by_id(_id)
        if order:
            return order.json()
        return {'message': 'Item not found'}, 404


class UserOrders(Resource):
    def get(self, user_id):
        return list(map(lambda x: x.json(), OrderModel.find_by_user_id(user_id)))

    def post(self, user_id):
        data = Order.parser.parse_args()

        order = OrderModel(data['confirmation_num'],
                           data['user_id'], data['total'])

        try:
            order.save_to_db()
        except:
            return {'message': 'An error ocurred inserting the order'}, 500

        created_order = order.json()
        order_id = created_order['id']

        order_list = []
        for _id in data['item_ids']:
            order_list.append(OrderItemModel(order_id, _id))

        for obj in order_list:
            obj.save_to_db()

        return order.json(), 201
