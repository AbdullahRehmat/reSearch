import json
import redis
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

redis_host = "redis-api"
redis_port = 6379
redis_password = "Password:)"


# Redis Database
r0 = redis.Redis(host=redis_host, port=redis_port,
                password=redis_password, db=0, decode_responses=True)

# Redis Streams
r1 = redis.Redis(host=redis_host, port=redis_port,
                password=redis_password, db=1, decode_responses=True)


class siteAPI_GP(Resource):

    # Returns existing Queries
    def get(self):
        queries = r0.get('queryDB')
        return {'data': queries}, 200

    # Adds new Query
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('query', required=True)

        args = parser.parse_args()
        r0.set('queryDB', str(args))

        # Add message to stream
        return {'data': args}, 201


class test_API(Resource):

    # API Route for Testing
    def get(self):
        r1.xadd('streamOne', {'msg': 'msgFromGetAPI'})


# Create routes
api.add_resource(siteAPI_GP, "/query")
api.add_resource(test_API, "/test")


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
