from flask import Flask
from flask_restful import Api, Resource, reqparse
from security import authenticate, identity
from flask_jwt import JWT, jwt_required
from models.item import ItemModel
import sqlite3

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                type=float,
                required=True,
                help="This field can not be blank!"
    )
    parser.add_argument('store_id',
                type=int,
                required=True,
                help="Every item needs a store id!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message":"Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message' : "An item with name {} already exists.".format(name)}, 400
        request_data = Item.parser.parse_args()
        item = ItemModel(name, request_data['price'], request_data['store_id'])
        item.save_to_db()
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if not item:
            return {'message' : 'item does not exists'}, 400
        
        item.delete_from_db()
        return {'message' : 'item deleted'}

    def put(self, name):
        """ Update resource, if resource doesnt exist, create a new one
        """
        request_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if not item:
            item = ItemModel(name, request_data['price'], request_data['store_id'])
        else:
            item.price = request_data['price']
        item.save_to_db()
        return item.json(), 201


class ItemList(Resource):
    def get(self):
        ## get a list of all item in json format
        items = [item.json() for item in ItemModel.query.all()]
        ## we can get the items list using lambda as well
        # items = list(map(lambda x : x.json(), ItemModel.query.all()))
        return {'items' : items}
        
