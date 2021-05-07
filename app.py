from flask import Flask, request

# Resource is something that our API represents
# For example, if our API is concerned with Students,
# it can create, delete or update Students => then our resource is a Student.

# Resources are usually mapped into database tables as well.

from flask_restful import Resource, Api, reqparse
# JWT -> JSON Web Token
from flask_jwt import JWT, jwt_required
from security import authenticate, identity


app = Flask(__name__)

app.secret_key = 'gurleen'
# The Api works with resources and every resource has to be a class.
api = Api(app)
# JWT creates a new endpoint -> /auth
jwt = JWT(app, authenticate, identity)

items = []


# Item Resource
class Item(Resource):
    # Using a parser to make sure only specific fields are updated.
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be empty.')

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': f'An item with the {name} already exists.'}, 400
        # If the request does not have JSON attached or
        # if the content-type is set wrong in the header,
        # the below line will give an error.
        # request_data = request.get_json()
        # To overcome that problem - 2 ways -
        # 1. pass force=True--> will process the data even if the content-type is not set.
        # 2. pass silent=True--> will just return None.

        request_data = Item.parser.parse_args()
        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        # No need to convert dictionary to JSON, flask_restful takes care of it.
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        request_data = Item.parser.parse_args()

        # request_data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        message = ''
        if item is None:
            # Add new item.
            item = {'name': name, 'price': request_data['price']}
            items.append(item)
            message = 'Item successfully added.'
        else:
            item.update(request_data)
            message = 'Item successfully updated.'
        return {'message': message}


class ItemList(Resource):
    def get(self):
        if len(items) == 0:
            return {'message': 'No items to see here.'}, 404
        return items


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
app.run(port=5000, debug=True)
# Before coding the apis create requests in postman, this will help in determining the api structures.

# Status codes -
# 200 request successful
# 404 resource not found
# 201 resource created
# 202 resource creation request accepted
# 400 bad request
