import json
import redis
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

redis_host = "redis-api"
redis_port = 6379
redis_password = "Password:)"

r = redis.Redis(host=redis_host,
                port=redis_port,
                password=redis_password,
                db=0)


class siteAPI_GP(Resource):

    # Returns existing Queries
    def get(self):

        queries = r.get('queryDB').decode('utf-8')
        return {'message': 'Success', 'data': queries}, 200

    # Adds new Query
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('identifier', required=True)
        parser.add_argument('query', required=True)

        args = parser.parse_args()

        r.set('queryDB', str(args))
        return {'message': 'Query Recieved', 'data': args}, 201


# Create routes
api.add_resource(siteAPI_GP, "/query")

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
