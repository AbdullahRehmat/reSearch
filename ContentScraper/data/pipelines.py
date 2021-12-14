# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import pymongo
from itemadapter import ItemAdapter
from scrapy.http.request.form import _urlencode
from ..SpellChecker.app import SpellChecker

# class DataPipeline:
#    def process_item(self, item, spider):
#        return item


class MongoPipeline(object):

    collection_name = 'ScrapedData-C1'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # Pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        # Initializing spider
        # Opening DB connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

        # Drop Old Database To Prevent Duplicates
        self.db[self.collection_name].drop()

    def close_spider(self, spider):
        # Clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):

        # Item <- Dict
        # Item["title"] <- Set
        # Item["url"] <- Set
        # Item["source"] <- Str

        # Spell Check Title
        s = SpellChecker()
        item["title"] = [s.spell_checker(str(item["title"][0]))]

        self.db[self.collection_name].insert(dict(item))
        logging.debug("Post added to MongoDB")

        return item
