from flask import Flask, request
import datetime
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.secret_key = 'sumit'
api = Api(app)
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=1) ## default jwt token expiration is 5 min.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False


## https://pythonhosted.org/Flask-JWT/
jwt = JWT(app, authenticate, identity)  ## it will create an endpoint :  /auth

@app.before_first_request
def create_table():
    """ This will create all tables and db just after app is initialized.
    Its automatically create required table by just going through import statements in app.py
    """
    db.create_all()


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
#api.add_resource(Item, '/items')

if __name__ == "__main__":
    from database import db
    db.init_app(app)
    app.run(port=5000, debug=True)
