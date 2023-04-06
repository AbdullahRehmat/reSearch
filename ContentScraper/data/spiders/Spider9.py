from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderNine(Spider):
    name = "data"

    allowed_domains = [
        "www.wahhabis.com",
    ]

    start_urls = [
        "http://www.wahhabis.com/authors/Abu.Iyaad.cfm",
        "http://www.wahhabis.com/authors/Abu.Iyaad.cfm?start=31",
        "http://www.wahhabis.com/authors/admin.cfm",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get()
            item['source'] = 'Wahhabis.com - Article - Abu Iyaad'
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item
