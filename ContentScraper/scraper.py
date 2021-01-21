# Import Modules
import redis
import scrapy
import pymongo

# Environment Variables
redis_host = "redis-api"
redis_port = 6379
redis_password = "Password:)"

# Connect to Redis Streams


# Connect to DB


# Scrapy Script
class ArticleSpider(scrapy.Spider):
    name = "articles"

    start_urls = [
        'http://www.shia.bs/articles/lvrahxj-shiite-fatwa-for-killing-of-sunni-muslims-to-attain-paradise.cfm'
    ]

    def parse(self, response):
        SET_SELECTOR = '.articleTitle'
        for title in response.css(SET_SELECTOR):
            NAME_SELECTOR = '.articleTitle::text'
            yield {
                'name': title.css(NAME_SELECTOR).get(),
            }

# Save Output to DB


# NOTES
# http://www.shia.bs/articles/lvrahxj-shiite-fatwa-for-killing-of-sunni-muslims-to-attain-paradise.cfm
# response.css('.articleTitle::text').get()
