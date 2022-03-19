import os
import redis
import pymongo
from dotenv import load_dotenv
from rank_bm25 import BM25Plus
from redis.commands.json.path import Path as JPath


class Corpus():
    def __init__(self, mongo_col) -> None:
        self.col = mongo_col
        self.corpus = []

    def create_corpus(self) -> None:
        """ Creates Corpus Of Titles From A MongoDB Collection"""

        for data in self.col.find():
            self.corpus += data["title"]

        return self.corpus


class SearchEngine():
    def __init__(self, mongo_col_1, mongo_col_2, redis, corpus, stream_data) -> None:
        self.colA = mongo_col_1
        self.colB = mongo_col_2
        self.rdb = redis
        self.stream = stream_data
        self.corpus = corpus
        self.id = ""
        self.query = ""
        self.title = ""
        self.url_html = ""
        self.url_json = {}
        self.results_html = []
        self.results_json = []

    def parse_stream(self) -> None:
        """ Parses Information From Redis Stream Message """

        s = self.stream[0][1][0][1]
        self.id = s["identifier"]
        self.query = s["query"]

    def format_url(self) -> None:
        """ Formats Titles & URLs Into Valid HTML Links """

        # Get Title's URL & Source
        data = self.colB.find_one({"title": self.title}, {
            "_id": 0, "url": 1, "source": 1})
        url = data["url"]
        source = data["source"][0]

        # Format Results as HTML
        self.url_html = f"<a href=\" {url} \" class=\"searchResult\" target=\"_blank\" rel=\"noopener noreferrer\"> {self.title} <br/> <p class=\"resultSource\"> {source} </p> </a><br />"

        # Format As JSON
        self.url_json = {
            "title": self.title,
            "url": data["url"],
            "source": data["source"][0]
        }

    def search_engine(self) -> None:
        """Ranks Corpus According To Query Via BM25"""

        # Convert Query To Upper Case To Improve Search Results
        query = self.query.title()

        # BM25 Configuration
        tokenized_query = query.split(" ")
        tokenized_corpus = [title.split(" ") for title in self.corpus]
        bm25 = BM25Plus(tokenized_corpus)

        # Return "n" Most Relevant Titles
        ranked_titles = list(bm25.get_top_n(
            tokenized_query, self.corpus, n=30))

        # Iterate Through Ranked Titles + Format
        for title in ranked_titles:
            self.title = title
            self.format_url()
            self.results_html += [self.url_html]
            self.results_json += [self.url_json]

    def send_results(self):
        """Sends JSON Formatted Results To API Via Redis"""

        data = {
            "id": self.id,
            "query": self.query,
            # "results": self.html_results
            "results": self.results_json
        }

        # Return Results To API Via REDIS DB1
        self.rdb.json().set(str("id:" + self.id), JPath.rootPath(), data)

        # Add Results To MongoDB Col1
        # ONLY USED BY METRIX SERVICE
        self.colA.insert_one({"_id": self.id, "data": [self.results_html]})


if __name__ == "__main__":
    # Load .env Variables From File
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
    c = Corpus(col2)
    c = c.create_corpus()

    # Block Stream To Wait For Incomming Message
    while True:
        stream = rdb0.xread({'streamA': "$"}, count=1, block=0)

        if stream != {}:
            s = SearchEngine(col1, col2, rdb1, c, stream)
            s.parse_stream()
            s.search_engine()
            s.send_results()
