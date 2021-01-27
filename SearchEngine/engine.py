import redis
import json
import pymongo
from rank_bm25 import BM25Okapi

# Environment Variables
redis_host = "redis-api"
redis_port = 6379
redis_password = "Password:)"

mongo_host_1 = "mongo-se"
mongo_host_2 = "mongo-cs"
mongo_port = 27017

# Connect to Redis Streams
r1 = redis.Redis(host=redis_host, port=redis_port,
                 password=redis_password, db=1, decode_responses=True)

# Connect to MongoSE Database
conn1 = pymongo.MongoClient(
    host='mongodb://' + mongo_host_1 + ':' + str(mongo_port) + '/')
db1 = conn1["SearchEngineData"]

# Connect to MongoCS Database
conn2 = pymongo.MongoClient(
    host='mongodb://' + mongo_host_2 + ':' + str(mongo_port) + '/')
db2 = conn2["testDatabase"]
col2 = db2["testCollection"]

# BM25 Configuration


# Redis Streams
while True:
    fromStreamA = r1.xread({'streamA': "$"}, count=1, block=0)

    if fromStreamA != {}:

        # Get Query from StreamA as String FIX ME
        streamQuery = fromStreamA[0][1][0][1]
        streamQuery = streamQuery["query"]

        # Get Titles from DB | Copy to Corpus
        corpus = []
        for data in col2.find():
            corpus += data["title"]

        # Move Query from StreamA to BM25
        query = streamQuery

        # BM25 Config
        tokenized_query = query.split(" ")

        tokenized_corpus = [doc.split(" ") for doc in corpus]
        bm25 = BM25Okapi(tokenized_corpus)

        # Return 10 most relavent Titles [n=10]
        rankedResults = bm25.get_top_n(tokenized_query, corpus, n=10)

        # HTML + Title + URL List 
        responseDict = []

        # For List of ranked Titles:
        for result in rankedResults:
            # Find Title in DB

            queryDict = {"title": result}
            # Get Title
            title = result
            # Get Title's URL
            url = col2.find_one(queryDict, {"_id": 0, "url": 1})
            url = url["url"]

            # Format Results with HTML tags
            htmlResponse = "<a href=\"" + \
                url + "\" class=\"searchResult\">" + title + "</a>"

            responseDict += [htmlResponse]

    # Return Results via Redis StreamB to GlobalAPI
    r1.xadd('streamB', {'data': str(responseDict)})
