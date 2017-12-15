from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.favorite import FavoriteModel
import logging


class Favorite(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=int, required=True)
    parser.add_argument('item_id', type=int, required=True)

    def get(self, user_id):
        return list(map(lambda x: x.json(), FavoriteModel.find_by_user_id(user_id)))

    def post(self, user_id):
        data = Favorite.parser.parse_args()

        favorite = FavoriteModel(**data)

        logging.warning(data)

        try:
            favorite.save_to_db()
        except:
            return {'message': 'An error occured inserting the favorite'}, 500

        return favorite.json_favorite(), 201

    def delete(self, _id):
        favorite = FavoriteModel.find_by_id(_id)
        if favorite:
            favorite.delete_from_db()

        return {'message': 'Favorite deleted'}
