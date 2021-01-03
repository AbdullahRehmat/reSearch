from flask import Flask, request, g
from flask_restful import Resource, Api, reqparse
import shelve
import redis


app = Flask(__name__)
api = Api(app)

redis_host = "redis"
redis_port = 6379
redis_password = "Password:)"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("queries.db")
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


class siteAPI_GP(Resource):

    # Returns existing Queries
    def get(self):

        shelf = get_db()
        keys = list(shelf.keys())

        queries = []

        for key in keys:
            queries.append(shelf[key])

        return {'message': 'Success', 'data': queries}, 200

    # Adds new Query
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('identifier', required=True)
        parser.add_argument('query', required=True)

        args = parser.parse_args()

        shelf = get_db()
        shelf[args['identifier']] = args

        return {'message': 'Query Recieved', 'data': args}, 201


class siteAPI_DB(Resource):
    def get(self, identifier):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        if not (identifier in shelf):
            return {'message': 'Device not found', 'data': {}}, 404

        return {'message': 'Device found', 'data': shelf[identifier]}, 200

    def delete(self, identifier):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        if not (identifier in shelf):
            return {'message': 'Device not found', 'data': {}}, 404

        del shelf[identifier]
        return '', 204


# Create routes
api.add_resource(siteAPI_GP, "/")
api.add_resource(siteAPI_DB, '/db/<string:identifier>')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
