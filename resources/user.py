
from flask_restful import Resource, reqparse
from flask import Flask, request
import sqlite3
from models.user import UserModel
    
class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
            type=str,
            required=True,
            help="This field can not be blank."
            )
    
    parser.add_argument('password',
            type=str,
            required=True,
            help="This field can not be blank."
            )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "user already exists"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()
        return {"message" : "user created successfully"}, 201


