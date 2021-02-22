from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderFourteen(Spider):
    name = "data"

    allowed_domains = [
        "www.islamjesus.ws",
    ]

    start_urls = [
        "http://www.islamjesus.ws/authors/Abu.Iyaad.cfm",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get(),
            item['source'] = 'IslamJesus.ws - Article - Abu Iyyad',
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item