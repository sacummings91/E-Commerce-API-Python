from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.order import OrderModel


class Order(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('confirmation_num', type=float, required=True)
    parser.add_argument('user_id', type=int, required=True)
    parser.add_argument('total', type=float, required=True)

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

        order = OrderModel(**data)

        try:
            order.save_to_db()
        except:
            return {'message': 'An error ocurred inserting the order'}, 500

        return order.json(), 201
