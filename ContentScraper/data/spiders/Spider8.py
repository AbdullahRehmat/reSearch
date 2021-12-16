from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderEight(Spider):
    name = "data"

    allowed_domains = [
        "www.islamagainstextremism.com",
    ]

    start_urls = [
        "http://www.islamagainstextremism.com/authors/Admin.cfm",
        "http://www.islamagainstextremism.com/authors/Admin.cfm?start=31",
        "http://www.islamagainstextremism.com/authors/Admin.cfm?start=61",
        "http://www.islamagainstextremism.com/authors/Admin.cfm?start=91",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get(),
            item['source'] = 'IslamAgainstExtremism.com - Article - Abu Iyyad',
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item
