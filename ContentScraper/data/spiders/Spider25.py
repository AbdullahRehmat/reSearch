from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderEighteen(Spider):
    name = "data"

    allowed_domains = [
        "www.abovethethrone.com",
    ]

    start_urls = [
        "https://www.islamhomosexuality.com/hs/authors/Admin.cfm",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleList')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleList::text').get()
            item['source'] = 'IslamHomosexuality.com - Article - Abu Iyyad'
            item['url'] = data.css('a.articleTitleList::attr(href)').get()
            yield item
