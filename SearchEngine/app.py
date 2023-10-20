"""
    BM25 Based Search Engine Microservice That Ranks
    Corpus According To Latest Query Recieved Via Redis
    Streams.
"""

import os
import time
import redis
import pymongo
from dotenv import load_dotenv
from rank_bm25 import BM25Plus
from redis.commands.json.path import Path
from spellchecker import SpellChecker


class Corpus():
    def __init__(self, mongo_col) -> None:
        self.col = mongo_col
        self.corpus = []

    def correct_titles(self) -> None:
        """ Corrects Spelling Of Titles In MongoDB Col """

        s = SpellChecker()

        # Collect Title From Col & Append To Corpus
        for data in self.col.find():
            self.corpus.append(data["title"])

        for title in self.corpus:
            new_title = s.run_spell_checker(title)

            if new_title == title:
                pass

            else:
                self.col.update_one({"title": title}, {
                                    "$set": {"title": new_title}})

        # Empty Corpus
        del self.corpus[:]

        return None

    def create_corpus(self) -> None:
        """ Creates Corpus Of Titles From MongoDB Collection"""

        # Empty Corpus
        del self.corpus[:]

        for data in self.col.find():
            self.corpus.append(data["title"])

        return None

    def yield_corpus(self) -> list:
        """ Returns Corpus As List Of Titles """

        return self.corpus


class SearchEngine():
    def __init__(self, mongo_col, corpus, identifier, query) -> None:
        self.mongo_col = mongo_col
        self.identifier = identifier
        self.query = query
        self.corpus = corpus
        self.max_results = 45           # Number Of Results Returned
        self.ranked_corpus = ()
        self.results = []

    def correct_query(self) -> None:
        """ Corrects Spelling Of Query """

        s = SpellChecker()
        self.query = s.run_spell_checker(self.query)

        return None

    def rank_corpus(self) -> None:
        """ Ranks Corpus According To Query"""

        # Convert Query To Upper Case To Improve Search Results
        query = self.query.title()

        # BM25 Configuration
        tokenized_query = query.split(" ")
        tokenized_corpus = [title.split(" ") for title in self.corpus]
        bm25 = BM25Plus(tokenized_corpus)

        # Return n Most Relevant Titles
        self.ranked_corpus = tuple(bm25.get_top_n(
            tokenized_query, self.corpus, self.max_results))

        return None

    def format_results(self) -> None:
        """ Formats Result's Title, URL & Source As Valid HTML5"""

        for title in self.ranked_corpus:

            # Get Title's URL & Source
            data = self.mongo_col.find_one(
                {"title": title}, {"_id": 0, "url": 1, "source": 1})

            # Format As JSON
            result = {
                "title": title,
                "url": data["url"],
                "source": data["source"]
            }

            self.results.append(result)

        return None

    def yield_results(self, time_taken_ms: int) -> dict:
        """ Returns Results Dict As Valid JSON """

        time_taken_ms = str(round(time_taken_ms, 2)) + " ms"

        results = {
            "id": self.identifier,
            "query": self.query,
            "time_taken": time_taken_ms,
            "results": self.results
        }

        return results


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
    c.correct_titles()          # Standardise Spelling Of All Titles
    c.create_corpus()           # Create Corpus Of Titles
    c = c.yield_corpus()        # Return Corpus

    # Block Redis Stream Until Message Arrives
    while True:
        stream = rdb0.xread({'streamA': "$"}, count=1, block=0)

        if stream != {}:

            # Parse Stream Data
            identifier = stream[0][1][0][1]["identifier"]
            query = stream[0][1][0][1]["query"]

            # Start Query Timer
            start_time = time.perf_counter()

            # Call Search Engine
            s = SearchEngine(col1, c, identifier, query)

            s.correct_query()       # Standardise Query Spelling
            s.rank_corpus()         # Rank Corpus According To Query
            s.format_results()      # Format Results As JSON

            # Calculate Time Taken In Milliseconds
            time_taken_ms = (time.perf_counter() - start_time) * 1000

            # Provide Time Taken & Collect Results
            results = s.yield_results(time_taken_ms)

            # Return Results To API
            rdb1.json().set(str("id:" + identifier), Path.root_path(), results)

            # Add Results To MongoDB Collection
            # ONLY USED BY METRIX SERVICE
            col2.insert_one(
                {"_id": identifier, "query": query, "data": results})
