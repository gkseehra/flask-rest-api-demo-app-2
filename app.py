from flask import Flask

# Resource is something that our API represents
# For example, if our API is concerned with Students,
# it can create, delete or update Students => then our resource is a Student.

# Resources are usually mapped into database tables as well.

from flask_restful import Resource, Api

app = Flask(__name__)
# The Api works with resources and every resource has to be a class.
api = Api(app)

items = []


# Item Resource
class Item(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item
        return {'item': None}, 404

    def post(self, name):
        item = {'name': name, 'price': 13.99}
        items.append(item)
        # No need to convert dictionary to JSON, flask_restful takes care of it.
        return item, 201


api.add_resource(Item, '/item/<string:name>')

app.run(port=5000, debug=True)
# Before coding the apis create requests in postman, this will help in determining the api structures.

# Status codes -
# 200 request successful
# 404 resource not found
# 201 resource created
# 202 resource creation request accepted
