from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderThree(Spider):
    name = "data"

    allowed_domains = [
        "www.salafis.com",
    ]

    start_urls = [
        "http://www.salafis.com/authors/Abu.Iyaad.cfm",
        "http://www.salafis.com/authors/Abu.Iyaad.cfm?start=31",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get()
            item['source'] = 'Salafis.com - Article - Abu Iyyad'
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item
