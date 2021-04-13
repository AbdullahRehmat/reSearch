import os
import redis
import json
import pymongo
from dotenv import load_dotenv
from rank_bm25 import BM25Okapi
import asyncio

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

# Connect to Redis Streams
r0 = redis.Redis(host=redis_host, port=redis_port,
                 password=redis_password, db=0, decode_responses=True)

r1 = redis.Redis(host=redis_host, port=redis_port,
                 password=redis_password, db=1, decode_responses=True)

# Connect to MongoSE Database
conn1 = pymongo.MongoClient(
    host='mongodb://' + mongo_host_1 + ':' + str(mongo_port) + '/')
db1 = conn1[mongo_db_1]
col1 = db1[mongo_col_1]

# Connect to MongoCS Database
conn2 = pymongo.MongoClient(
    host='mongodb://' + mongo_host_2 + ':' + str(mongo_port) + '/')
db2 = conn2[mongo_db_2]
col2 = db2[mongo_col_2]


class searchEngine():

    # Get Titles from MongoCS + Return as Corpus
    def createCorpus():
        corpus = []
        for data in col2.find():
            corpus += data["title"]
        return corpus

    # Outputs Title formatted with HTML + Other relavent information
    def htmlResponse(col2, title):
        # Get Title's URL + Source
        dbResponse = col2.find_one(
            {"title": title}, {"_id": 0, "url": 1, "source": 1})
        url = dbResponse["url"]
        source = dbResponse["source"][0]

        # Format Results with HTML tags
        htmlResponse = f"<a href=\" {url} \" class=\"searchResult\" target=\"_blank\" rel=\"noopener noreferrer\"> {title} <br/> <p class=\"resultSource\"> {source} </p> </a><br />"
        return htmlResponse

    # Takes query as input, returns sorted search results to Redis & MongoDB
    def engine(col1, r1, streamAData):
        # Get Query from StreamA as String
        streamData = streamAData[0][1][0][1]
        streamQuery = streamData["query"]
        streamIdentifier = streamData["identifier"]

        # Move Query from StreamA to BM25
        # Converts Query to Uppercase to improve search results
        query = str(streamQuery).title()

        # BM25 Config
        tokenized_query = query.split(" ")
        tokenized_corpus = [doc.split(" ") for doc in corpus]
        bm25 = BM25Okapi(tokenized_corpus)

        # Return n most relavent Titles
        rankedTitles = bm25.get_top_n(tokenized_query, corpus, n=25)

        # HTML + Title + URL List
        responseList = []
        responseDict = {}

        # For List of ranked Titles:
        for title in rankedTitles:

            response = searchEngine.htmlResponse(col2, title)
            responseList += [response]

            # Add List to Dict <- MongoDb Col1
            responseDict['_id'] = streamIdentifier
            responseDict['data'] = [responseList]

        # Return Results via Redis DB1 to GlobalAPI
        r1.set(streamIdentifier, str(responseList), ex=300)

        # Add Results to MongoDB Col1
        # Currently used by MetriX Service Only
        col1.insert_one(responseDict)


# Runs at Start of Script to decrease Search time + DB Calls
corpus = searchEngine.createCorpus()


# Redis Streams
while True:
    streamAData = r0.xread({'streamA': "$"}, count=1, block=0)

    if streamAData != {}:
        # Process query via Engine Function
        searchEngine.engine(col1, r1, streamAData)
