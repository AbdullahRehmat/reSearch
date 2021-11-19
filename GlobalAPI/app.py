import os
import time
import redis
import pymongo
from ast import literal_eval
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Resource, Api, reqparse

# Init Flask & API
app = Flask(__name__)
api = Api(app)

# Load ENV Variables
load_dotenv()

# Redis .env Variables
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_password = os.getenv("REDIS_PASSWORD")

# MongoDB General Settings
mongo_port = os.getenv("MONGO_PORT")

# MongoDB DB1 .env Variables
mongo_host_1 = os.getenv("MONGO_HOST_1")
mongo_db_1 = os.getenv("MONGO_DB_1")
mongo_col_1 = os.getenv("MONGO_COL_1")

# MongoDB DB2 .env Variables
mongo_host_2 = os.getenv("MONGO_HOST_2")
mongo_db_2 = os.getenv("MONGO_DB_2")
mongo_col_2 = os.getenv("MONGO_COL_2")

# Redis Streams
r0 = redis.Redis(host=redis_host, port=redis_port,
				 password=redis_password, db=0, decode_responses=True)

r1 = redis.Redis(host=redis_host, port=redis_port,
				 password=redis_password, db=1, decode_responses=True)

# Connect to MongoSE Database
conn1 = pymongo.MongoClient(
	host='mongodb://' + mongo_host_1 + ':' + str(mongo_port) + '/')
db1 = conn1[mongo_db_1]
col1 = db1[mongo_col_1]

conn2 = pymongo.MongoClient(
	host='mongodb://' + mongo_host_2 + ':' + str(mongo_port) + '/')
db2 = conn2[mongo_db_2]
col2 = db2[mongo_col_2]


def redis_results(identifier):
	data = r1.get(identifier)
	data = literal_eval(data)
	return data


def mongo_results(identifier):
	for i in col1.find({"_id": identifier}):
		data = i['data'][0]
		return data


class QueryAPI(Resource):
	"""
	Route for API to recieve requests on

	"""

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('identifier', required=True)
		parser.add_argument('query', required=True)
		args = parser.parse_args()

		# Add message to Stream -> SearchEngine
		r0.xadd('streamA', fields=args)

		# Return Data to Site
		return {'message': 'Success', 'data': args}, 202


class ResultsAPI(Resource):
	"""
	Returns results collected from MongoDB Database to Client

	"""

	def get(self, identifier):
		time.sleep(0.5)

		# Get Results from Redis DB0
		results = redis_results(identifier=identifier)

		# Return Results
		return results, 200


class Metrix(Resource):
	"""
	Collect usage statistics from MongoDB Database and return to Website

	"""

	def get(self):
		# Get Statistics from Databases
		db1Count = col1.estimated_document_count()
		db2Count = col2.estimated_document_count()
		db3Count = r1.dbsize()

		# Format Statistics
		response = {"totalQueryCount": db1Count,
					"totalArticleCount": db2Count,  "liveQueryCount": db3Count}

		# Return Results
		return response, 200


# Create routes
api.add_resource(QueryAPI, "/api/v1/query")
api.add_resource(ResultsAPI, "/api/v1/results/<identifier>")
api.add_resource(Metrix, "/api/v1/metrix")
