from flask_restful import Resource, reqparse
from models.order import OrderModel
from models.order_item import OrderItemModel


class Order(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('confirmation_num', type=float, required=True)
    parser.add_argument('user_id', type=int, required=True)
    parser.add_argument('total', type=float, required=True)
    parser.add_argument('item_ids', type=int, action='append', required=True)

    def get(self, _id):
        order = OrderModel.find_by_id(_id)
        if order:
            return order.json()
        return {'message': 'Item not found'}, 404


class UserOrders(Resource):
    def get(self, user_id):
        user_orders = list(
            map(lambda x: x.json(), OrderModel.find_by_user_id(user_id)))

        order_ids = []

        for i in user_orders:
            order_ids.append(i['id'])

        order_items = OrderItemModel.find_by_order_id(order_ids)
        json_order_items = list(
            map(lambda x: x.json_order_item(), order_items))

        json_order_info = {}
        json_order_info['userOrders'] = user_orders
        json_order_info['orderItems'] = json_order_items

        return json_order_info

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
