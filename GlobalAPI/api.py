import json
import redis
import requests
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pymongo
import time

app = Flask(__name__)
api = Api(app)

redis_host = "redis-api"
redis_port = 6379
redis_password = "Password:)"

mongo_host_1 = "mongo-se"
mongo_port = 27017

# Redis Database
r0 = redis.Redis(host=redis_host, port=redis_port,
                 password=redis_password, db=0, decode_responses=True)

# Redis Streams
r1 = redis.Redis(host=redis_host, port=redis_port,
                 password=redis_password, db=1, decode_responses=True)

# Connect to MongoSE Database
conn1 = pymongo.MongoClient(
    host='mongodb://' + mongo_host_1 + ':' + str(mongo_port) + '/')
db1 = conn1["SearchEngineDB"]
col1 = db1["htmlResults"]


def find_MongoSE(identifier):
    for i in col1.find({"_id": identifier}):
        data = i['data'][0]
        return data


class queryAPI(Resource):

    def get(self):  # Send Results
        parser = reqparse.RequestParser()
        parser.add_argument('identifier', required=True)
        args = parser.parse_args()

        # Parse Identifier from args
        identifier = args.get('identifier')

        # Get Results from MongoSe
        time.sleep(0.07)
        results = find_MongoSE(identifier=identifier)

        # Return Results
        return results, 200

    def post(self):  # Reveive Query
        parser = reqparse.RequestParser()
        parser.add_argument('identifier', required=True)
        parser.add_argument('query', required=True)
        args = parser.parse_args()

        # Save Query to RedisDB
        r0.set('queryDB', str(args))

        # Add message to Stream
        r1.xadd('streamA', fields=args)

        # Return Data to Site
        return {'data': args}, 202
   
class matrix(Resource):

    def get(self):
        queryCount = col1.estimated_document_count()
        return queryCount, 200

# Create routes
api.add_resource(queryAPI, "/api")
api.add_resource(matrix, "/matrix")


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
