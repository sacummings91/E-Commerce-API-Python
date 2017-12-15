from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from models.user import UserModel
from models.item import ItemModel
from models.favorite import FavoriteModel
import logging


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('last_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('role', type=str)

    def get(self, _id):
        user = UserModel.find_by_id(_id)
        json_user = user.json_user()

        favorites = FavoriteModel.find_by_user_id(_id)
        json_favorites = list(map(lambda x: x.json_favorite(), favorites))

        fav_item_ids = []

        for f in json_favorites:
            fav_item_ids.append(f['itemId'])

        favorite_items = ItemModel.find_by_fav_id(fav_item_ids)
        json_items = list(map(lambda x: x.json_item(), favorite_items))

        json_user['favorites'] = json_favorites
        json_user['favoriteItems'] = json_items

        return json_user

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201
