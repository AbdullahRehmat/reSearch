import scrapy
from scrapy import Selector


class TestSpider(scrapy.Spider):
    name = 'testspider'

    start_urls = ["https://www.salafisounds.com/category/speakers/"]

    def parse(self, response):
        scrapedData = Selector(response).css('h3.mh-posts-grid-title')

        for data in scrapedData:
            title = data.css('h3.mh-posts-grid-title > a::attr(title)').get()
            url = data.css('h3.mh-posts-grid-title > a::attr(href)').get()

        print(" ")
        print("#"*25)
        print(title)
        print(url)
        print("#"*25)
        print(" ")
