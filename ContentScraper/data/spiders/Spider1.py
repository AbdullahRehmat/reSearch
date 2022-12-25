from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderOne(Spider):
    name = "data"

    allowed_domains = [
        "www.shia.bs",
    ]

    start_urls = [
        "http://www.shia.bs/authors/Admin.cfm",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:

            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get()
            item['source'] = 'Shia.bs - Article - Abu Iyyad'
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item
