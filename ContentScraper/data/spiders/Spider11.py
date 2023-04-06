from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderEleven(Spider):
    name = "data"

    allowed_domains = [
        "www.ikhwanis.com",
    ]

    start_urls = [
        "http://www.ikhwanis.com/authors/Abu.Iyaad.cfm",
        "http://www.ikhwanis.com/authors/Abu.Iyaad.cfm?start=31",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get()
            item['source'] = 'Ikhwanis.com - Article - Abu Iyaad'
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item
