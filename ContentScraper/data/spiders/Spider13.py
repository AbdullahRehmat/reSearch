from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderThirteen(Spider):
    name = "data"

    allowed_domains = [
        "www.nabahani.com",
    ]

    start_urls = [
        "http://www.nabahani.com/authors/Abu.Iyaad.cfm",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get(),
            item['source'] = 'Nabahani.com - Article - Abu Iyyad',
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item
