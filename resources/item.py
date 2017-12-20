from flask_restful import Resource, reqparse, inputs
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('category',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('is_featured',
                        type=inputs.boolean,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('image_URL',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    # @jwt_required()  # Can put jwt_required on any method to require jwt authorization
    def get(self, _id):
        item = ItemModel.find_by_id(_id)
        if item:
            return item.json_item()
        return {'message': 'Item not found'}, 404

    def post(self):
        data = Item.parser.parse_args()

        item = ItemModel(**data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error ocurred inserting the item."}, 500

        return item.json_item(), 201

    def delete(self, _id):
        item = ItemModel.find_by_id(_id)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, _id):

        data = Item.parser.parse_args()

        item = ItemModel.find_by_id(_id)

        if item is None:
            item = ItemModel(name, **data)
        if 'name' in data.keys():
            item.name = data['name']
        if 'description' in data.keys():
            item.description = data['description']
        if 'category' in data.keys():
            item.category = data['category']
        if 'is_featured' in data.keys():
            item.is_featured = data['is_featured']
        if 'price' in data.keys():
            item.price = data['price']
        if 'image_URL' in data.keys():
            item.image_URL = data['image_URL']

        item.save_to_db()

        return item.json_item()


class ItemList(Resource):
    def get(self):
        return list(map(lambda x: x.json_item(), ItemModel.query.all()))
