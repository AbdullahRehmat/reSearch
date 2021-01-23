import redis
import json
import pymongo
from rank_bm25 import BM25Okapi

# Environment Variables
redis_host = "redis-api"
redis_port = 6379
redis_password = "Password:)"

mongo_host = "mongo-se"
mongo_port = 27018

# Connect to Redis Streams
r1 = redis.Redis(host=redis_host, port=redis_port,
                 password=redis_password, db=1, decode_responses=True)

# Connect to MongoSE Database
mongodb = pymongo.MongoClient(host='mongodb://' + mongo_host + ':' + str(mongo_port) + '/')
db = mongodb["SearchEngineData"]

# Redis Streams
while True:
    fromStreamA = r1.xread({'streamA': "$"}, count=1, block=0)

    # TESTING: Do work on query and return results
    if fromStreamA != {}:
        print(fromStreamA)
        r1.xadd('streamB', {'data': 'message received'})
