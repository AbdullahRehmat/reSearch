import os
import redis
import pymongo
from dotenv import load_dotenv
from rank_bm25 import BM25Plus
from redis.commands.json.path import Path as JPath


def create_corpus(col) -> list:
    corpus = []
    for data in col.find():
        corpus += data["title"]

    return corpus


def url_formatter(col, title) -> str:
    """ Formats Titles & URLs Into Valid HTML Links """

    # Get Title's URL & Source from Col2
    db_data = col.find_one({"title": title}, {"_id": 0, "url": 1, "source": 1})
    url = db_data["url"]
    source = db_data["source"][0]

    # Format Results as HTML
    output = f"<a href=\" {url} \" class=\"searchResult\" target=\"_blank\" rel=\"noopener noreferrer\"> {title} <br/> <p class=\"resultSource\"> {source} </p> </a><br />"

    return output


def search_engine(col ,corpus, stream_data) -> None:

    # Parse Information From Stream
    stream_data = stream_data[0][1][0][1]
    stream_query = stream_data["query"]
    stream_identifier = stream_data["identifier"]

    # Convert Query To Upper Case To Improve Results
    query = str(stream_query).title()

    # BM25 Configuration
    tokenized_query = query.split(" ")
    tokenized_corpus = [title.split(" ") for title in corpus]
    bm25 = BM25Plus(tokenized_corpus)

    # Return "n" Most Relevant Titles
    ranked_titles = list(bm25.get_top_n(tokenized_query, corpus, n=30))

    # List Of HTML + Title + URL
    response_list = []
    response_dict = {}

    # Iterate Through Ranked Titles + Format
    for title in ranked_titles:
        response = url_formatter(col2, title)
        response_list += [response]

    # Return Results To API Via REDIS DB1
    data = {
        "id": stream_identifier,
        "query": stream_query,
        "results": response_list
    }

    rdb1.json().set(str("id:" + stream_identifier), JPath.rootPath(), data)

    # Add Results To MongoDB Col1
    # ONLY USED BY METRIX SERVICE
    col.insert_one({"_id": stream_identifier, "data": [response_list]})

    return None


if __name__ == "__main__":
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
    # r0 -> Query Stream
    rdb0 = redis.Redis(host=redis_host, port=redis_port,
                       password=redis_password, db=0, decode_responses=True)

    # r1 -> Return Results To API
    rdb1 = redis.Redis(host=redis_host, port=redis_port,
                       password=redis_password, db=1, decode_responses=True)

    # Connect To MongoSE Database
    conn1 = pymongo.MongoClient(
        host=f"mongodb://{mongo_host_1}:{str(mongo_port)}/")
    db1 = conn1[mongo_db_1]
    col1 = db1[mongo_col_1]

    # Connect To MongoCS Database
    conn2 = pymongo.MongoClient(
        host=f"mongodb://{mongo_host_2}:{str(mongo_port)}/")
    db2 = conn2[mongo_db_2]
    col2 = db2[mongo_col_2]

    # Create Corpus
    corpus = create_corpus(col2)

    while True:
        streamData = rdb0.xread({'streamA': "$"}, count=1, block=0)

        if streamData != {}:
            search_engine(col1, corpus, streamData)
