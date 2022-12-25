from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderFifteen(Spider):
    name = "data"

    allowed_domains = [
        "www.ibntaymiyyah.com",
    ]

    start_urls = [
        "http://www.ibntaymiyyah.com/authors/Abu.Iyaad.cfm",
        "http://www.ibntaymiyyah.com/authors/Abu.Iyaad.cfm?start=31",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get()
            item['source'] = 'IbnTaymiyyah.com - Article - Abu Iyyad'
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item
