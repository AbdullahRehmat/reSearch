import os
import time
import redis
import pymongo
from dotenv import load_dotenv
from rank_bm25 import BM25Plus

load_dotenv()

# Redis .env Variables
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_password = os.getenv("REDIS_PASSWORD")

# MongoDB General Settings
mdb_port = os.getenv("MDB_PORT")

# MongoDB DB1 .env Variables
mdb_host_1 = os.getenv("MDB_HOST_1")
mdb_db_1 = os.getenv("MDB_DB_1")
mongo_col_1 = os.getenv("MDB_COL_1")

# MongoDB DB2 .env Variables
mdb_host_2 = os.getenv("MDB_HOST_2")
mdb_db_2 = os.getenv("MDB_DB_2")
mdb_col_2 = os.getenv("MDB_COL_2")


class Corpus():

    def __init__(self, input_col) -> None:
        self.col = input_col

    def create_corpus(self) -> list:
        """ Creates Corpus of Titles from MongoCS """

        corpus = []
        for data in self.col.find():
            corpus += data["title"]
        return corpus


class SearchEngine():

    def __init__(self, rdb1, output_col, input_col, corpus, stream_data) -> None:
        self.rdb1 = rdb1
        self.col1 = output_col
        self.col2 = input_col
        self.corpus = corpus
        self.stream_data = stream_data
        self.title = ""

    def url_formatter(self) -> str:
        """ Formats Titles + URLs Into Valid HTML Links """

        # Get Title's URL + Source from Col2
        db_data = self.col2.find_one(
            {"title": self.title}, {"_id": 0, "url": 1, "source": 1})
        url = db_data["url"]
        source = db_data["source"][0]

        # Format Results as HTML
        ouput = f"<a href=\" {url} \" class=\"searchResult\" target=\"_blank\" rel=\"noopener noreferrer\"> {self.title} <br/> <p class=\"resultSource\"> {source} </p> </a><br />"
        return ouput

    def engine(self) -> None:
        """Sorts Corpus By Query via BM25"""

        # Get Data from StreamA as Strings
        stream_data = self.stream_data[0][1][0][1]
        stream_query = stream_data["query"]
        stream_id = stream_data["identifier"]

        # Move Query from StreamA to BM25
        # Converts Query to Uppercase to improve search results
        query = str(stream_query).title()

        # BM25 Config
        tokenized_query = query.split(" ")
        tokenized_corpus = [doc.split(" ") for doc in self.corpus]
        bm25 = BM25Plus(tokenized_corpus)

        # Return n most relavent Titles
        # Lists used over Sets as order of results matters!
        ranked_titles = list(bm25.get_top_n(
            tokenized_query, self.corpus, n=30))

        # HTML + Title + URL List
        response_list = []
        response_dict = {}

        # Iterate through Ranked Titles + Format
        for title in ranked_titles:

            self.title = title
            response = self.url_formatter()
            response_list += [response]

            # Add List to Dict <- MongoDB Col1
            response_dict['_id'] = stream_id
            response_dict['data'] = [response_list]

        # Return Results via Redis DB1 to API
        self.rdb1.set(stream_id, str(response_list), ex=300)

        # Add Results to MongoDB Col1
        # Used by MetriX Service Only
        self.col1.insert_one(response_dict)

        return None


if __name__ == "__main__":

    # Connect to Redis Streams
    # r0 -> Query Stream
    rdb0 = redis.Redis(host=redis_host, port=redis_port,
                       password=redis_password, db=0, decode_responses=True)

    # r1 -> Return Results To API
    rdb1 = redis.Redis(host=redis_host, port=redis_port,
                       password=redis_password, db=1, decode_responses=True)

    # Connect To MongoSE Database
    conn1 = pymongo.MongoClient(
        host='mongodb://' + mdb_host_1 + ':' + str(mdb_port) + '/')
    db1 = conn1[mdb_db_1]
    col1 = db1[mongo_col_1]

    # Connect To MongoCS Database
    conn2 = pymongo.MongoClient(
        host='mongodb://' + mdb_host_2 + ':' + str(mdb_port) + '/')
    db2 = conn2[mdb_db_2]
    col2 = db2[mdb_col_2]

    c = Corpus(col2)
    c = c.create_corpus()

    # Monitor Redis Stream
    while True:
        streamAData = rdb0.xread({'streamA': "$"}, count=1, block=0)

        if streamAData != {}:
            # Pass Query To Search Engine
            s = SearchEngine(rdb1, col1, col2, c, streamAData)
            s.engine()
