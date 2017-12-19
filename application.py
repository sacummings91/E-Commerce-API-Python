from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.favorite import Favorite
from resources.order import Order, UserOrders
from resources.order_item import OrderItem
import os

application = Flask(__name__)
CORS(application)
# application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone_dev'
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ecommerceadmin:therealst33zy!!!@aazr52go8cnf2a.cxbnexrfclol.us-west-1.rds.amazonaws.com/capstone_dev'
# application.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.secret_key = 'h29fh09x9fha9w02h'
api = Api(application)


@application.before_first_request
def create_tables():
    db.create_all()


@application.before_request
def log_request_info():
    application.logger.debug('Headers: %s', request.headers)
    application.logger.debug('Body: %s', request.get_data())


jwt = JWT(application, authenticate, identity)  # /auth

api.add_resource(Item, '/item', '/item/<int:_id>')
api.add_resource(ItemList, '/items')
api.add_resource(Favorite, '/favorites/<int:_id>',
                 '/users/<int:user_id>/favorites')
api.add_resource(Order, '/orders/<int:_id>')
api.add_resource(UserOrders, '/users/<int:user_id>/orders')
api.add_resource(UserRegister, '/register', '/users/<int:_id>')
api.add_resource(OrderItem, '/orderitems/<int:order_id>')

if __name__ == '__main__':
    from db import db
    db.init_app(application)
    application.run(port=5000, debug=True)
