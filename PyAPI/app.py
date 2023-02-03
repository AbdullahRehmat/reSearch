"""
    Flask Based REST API That Forwards Incoming Query's To 
    The SearchEngine  Microservice & Returns Corresponding 
    Results As Valid JSON.
"""

import os
import time
import redis
import pymongo
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from redis.commands.json.path import Path as JPath

# Initialise Flask App
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Load Enviroment Variables
load_dotenv()

# API Information
api_name = os.getenv("API_NAME")
api_version = os.getenv("API_VERSION")

# Redis .env Variables
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_password = os.getenv("REDIS_PASSWORD")

# MongoDB General Settings
mongo_port = os.getenv("MONGO_PORT")
mongo_host = os.getenv("MONGO_HOST")
mongo_db_1 = os.getenv("MONGO_DB_1")
mongo_col_1 = os.getenv("MONGO_COL_1")
mongo_db_2 = os.getenv("MONGO_DB_2")
mongo_col_2 = os.getenv("MONGO_COL_2")

# Database Connection: Redis Streams
r0 = redis.Redis(host=redis_host, port=redis_port,
                 password=redis_password, db=0, decode_responses=True)

r1 = redis.Redis(host=redis_host, port=redis_port,
                 password=redis_password, db=1, decode_responses=True)

# Database Connection: MongoDB
conn = pymongo.MongoClient(
    host='mongodb://' + mongo_host + ':' + str(mongo_port) + '/')
db_1 = conn[mongo_db_1]
col1 = db_1[mongo_col_1]
db_2 = conn[mongo_db_2]
col2 = db_2[mongo_col_2]


def redis_results(identifier, id):
    """ Collects Results As JSON From Redis  """

    data = r1.json().get(str("id:" + identifier), JPath("." + id))

    return data


def mongo_results(identifier):
    """ Collects Results As JSON From MongoDB """

    for i in col1.find({"_id": identifier}):
        data = i['data'][0]

    return data

# Define API Routes


@app.route("/api/v1/")
def index():
    """ Provides API Usage Information """

    #
    # NEEDS TO BE IMPLEMENTED!
    #

    response = "reSearch Service: PyAPI - Version " + \
        str(api_version) + " <br/> https://github.com/AbdullahRehmat/reSearch/blob/main/Documentation/Documentation.md"

    return response, 200


@app.route("/api/v1/query", methods=["POST"])
def api_query():
    """ Receives Query From Client & Sends To SearchEngine"""

    identifier = request.json.get("identifier")
    query = request.json.get("query")

    if identifier == None and query == None:

        response = {
            "api": api_name,
            "version": api_version,
            "status": "ERROR: Identifier & Query Missing"
        }

        status_code = 400

    elif identifier == None:

        response = {
            "api": api_name,
            "version": api_version,
            "status": "ERROR: No Idenfitifer"
        }

        status_code = 400

    elif query == None:

        response = {
            "api": api_name,
            "version": api_version,
            "status": "ERROR: No Query",
        }

        status_code = 400

    else:
        status = "SUCCESS"
        status_code = 202

        data = {
            "identifier": identifier,
            "query": query
        }

        # Send Query: API -> Redis Stream -> SearchEngine
        r0.xadd("streamA", fields=data)

        response = {
            "api": api_name,
            "version": api_version,
            "status": status,
            "data": data
        }

    return jsonify(response), status_code


@app.route("/api/v1/results/<identifier>", methods=["GET"])
def api_results(identifier):
    """ Returns Results As JSON Provided Identifier Is Valid """

    if identifier == None:
        status = "ERROR: No Identifier"
        status_code = 400

        response = {
            "api": api_name,
            "version": api_version,
            "status": status
        }

    else:
        status = "SUCCESS"
        status_code = 200

        # Wait Until Results Appear In Redis DB
        while r1.exists("id:"+identifier) == 0:
            time.sleep(0.1)

        # Fetch Results From Redis
        query = redis_results(identifier, "query")
        results = redis_results(identifier, "results")
        time_taken = redis_results(identifier, "time_taken")

        response = {
            "api": api_name,
            "version": api_version,
            "status": status,
            "identifier": identifier,
            "time_taken": time_taken,
            "query": query,
            "results": results
        }

    return jsonify(response), status_code


@app.route("/api/v1/metrix", methods=["GET"])
def api_metrix():
    """ Returns Search Engine Usage Statistics """

    # Fetch Statistics From Databases
    db1Count = col1.estimated_document_count()
    db2Count = col2.estimated_document_count()
    db3Count = r1.dbsize()

    response = {
        "api": api_name,
        "version": api_version,
        "status": "SUCCESS",
        "data": {
            "liveQueries": db3Count,    # Queries That Have Not Timed Out
            "totalQueries": db1Count,   # Number Of Queries Processed By SearchEngine
            "totalArticles": db2Count   # Size Of SearchEngine Corpus
        }
    }

    return jsonify(response), 200
