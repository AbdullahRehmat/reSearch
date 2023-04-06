from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderFive(Spider):
    name = "data"

    allowed_domains = [
        "www.bidah.com",
    ]

    start_urls = [
        "http://www.bidah.com/authors/Abu.Iyaad.cfm",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get()
            item['source'] = 'Bidah.com - Article - Abu Iyaad'
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item
