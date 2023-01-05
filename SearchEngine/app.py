import os
import redis
import pymongo
import datetime
from dotenv import load_dotenv
from rank_bm25 import BM25Plus
from redis.commands.json.path import Path as JPath
from spellchecker import SpellChecker


class Corpus():
    def __init__(self, mongo_col) -> None:
        self.col = mongo_col
        self.corpus = []

    def correct_titles(self) -> None:
        """ Corrects Spelling Of Titles In MongoDB Col """

        s = SpellChecker()

        for data in self.col.find():
            self.corpus.append(data["title"])

        for title in self.corpus:
            new_title = s.spell_checker(title)

            if new_title == title:
                pass

            else:
                self.col.update_one({"title": title}, {
                                    "$set": {"title": new_title}})

        # Empty Corpus
        self.corpus = []

        return None

    def create_corpus(self) -> None:
        """ Creates Corpus Of Titles From MongoDB Collection"""

        for data in self.col.find():
            self.corpus.append(data["title"])

        return None

    def yield_corpus(self) -> list:
        """ Returns Corpus As List Of Titles """

        return self.corpus


class SearchEngine():
    def __init__(self, input_col, output_col, redis, stream_data, corpus) -> None:
        self.input_col = input_col
        self.output_col = output_col
        self.rdb = redis
        self.stream = stream_data
        self.corpus = corpus
        self.query_id = ""
        self.query = ""
        self.max_results = 30
        self.ranked_titles = ()
        self.results = []
        self.time_taken = None

    def parse_stream(self) -> None:
        """ Parses Redis Stream Message """

        s = self.stream[0][1][0][1]
        self.query_id = s["identifier"]
        self.query = s["query"]

        return None

    def correct_query(self) -> None:
        """ Corrects Spelling Of Query """

        s = SpellChecker()
        self.query = s.spell_checker(self.query)

        return None

    def rank_corpus(self) -> None:
        """ Ranks Corpus According To Query"""

        # Convert Query To Upper Case To Improve Search Results
        query = self.query.title()

        # BM25 Configuration
        tokenized_query = query.split(" ")
        tokenized_corpus = [title.split(" ") for title in self.corpus]
        bm25 = BM25Plus(tokenized_corpus)

        # Return Set Number Of Most Relevant Titles
        self.ranked_titles = tuple(bm25.get_top_n(
            tokenized_query, self.corpus, n=self.max_results))

        return None

    def format_results(self) -> None:
        """ Formats Result's Title, URL & Source"""

        for title in self.ranked_titles:

            # Get Title's URL & Source
            data = self.input_col.find_one({"title": title}, {
                "_id": 0, "url": 1, "source": 1})

            # Format As JSON
            result = {
                "title": title,
                "url": data["url"],
                "source": data["source"]
            }

            self.results.append(result)

        return None

    def send_results(self) -> None:
        """ Sends JSON Formatted Results To API Via Redis """

        results = {
            "id": self.query_id,
            "query": self.query,
            "time_taken": self.time_taken,
            "results": self.results
        }

        # Return Results To API Via REDIS DB1
        self.rdb.json().set(str("id:" + self.query_id), JPath.rootPath(), results)

        # Add Results To MongoDB Col1
        # ONLY USED BY METRIX SERVICE
        self.output_col.insert_one(
            {"_id": self.query_id, "query": self.query, "data": self.results})

        return None

    def run_search(self) -> None:
        """ Runs Complete Search & Times Functions """

        # Start Query Timer
        start_time = datetime.datetime.now()
        # Collect Query From Redis Stream
        self.parse_stream()
        # Correct Spelling Of Query
        self.correct_query()
        # Rank Corpus According To Query
        self.rank_corpus()
        # Format Most Relavant Titles From Corpus As HTML5
        self.format_results()
        # End Query Timer
        end_time = datetime.datetime.now() - start_time
        self.time_taken = str(float(end_time.microseconds / 1000)) + " ms"
        # Return Results
        self.send_results()

        return None


if __name__ == "__main__":
    # Load Enviroment Variables
    load_dotenv()

    redis_host = os.getenv("REDIS_HOST")
    redis_port = os.getenv("REDIS_PORT")
    redis_password = os.getenv("REDIS_PASSWORD")

    mongo_port = os.getenv("MONGO_PORT")
    mongo_host = os.getenv("MONGO_HOST")
    mongo_db_1 = os.getenv("MONGO_DB_1")
    mongo_col_1 = os.getenv("MONGO_COL_1")
    mongo_db_2 = os.getenv("MONGO_DB_2")
    mongo_col_2 = os.getenv("MONGO_COL_2")

    # Database Connection: Redis
    # r0 -> Incoming Query Stream
    rdb0 = redis.Redis(host=redis_host, port=redis_port,
                       password=redis_password, db=0, decode_responses=True)

    # r1 -> Return Results To API
    rdb1 = redis.Redis(host=redis_host, port=redis_port,
                       password=redis_password, db=1, decode_responses=True)

    # Database Connection: MongoDB
    conn = pymongo.MongoClient(
        host=f"mongodb://{mongo_host}:{str(mongo_port)}/")

    db1 = conn[mongo_db_1]      # ContentScraperDB
    col1 = db1[mongo_col_1]     # scrapedData
    db2 = conn[mongo_db_2]      # SearchEngineDB
    col2 = db2[mongo_col_2]     # returnedResults

    # Create Corpus
    c = Corpus(col1)
    c.correct_titles()
    c.create_corpus()
    c = c.yield_corpus()

    # Block Redis Stream & Wait For Incoming Message
    while True:
        stream_data = rdb0.xread({'streamA': "$"}, count=1, block=0)

        if stream_data != {}:
            s = SearchEngine(col1, col2, rdb1, stream_data, c)
            s.run_search()
