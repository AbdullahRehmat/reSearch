from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderNineteen(Spider):
    name = "data"

    allowed_domains = [
        "www.themadkhalis.com",
    ]

    start_urls = [
        "https://www.themadkhalis.com/md/authors/Admin.cfm",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get(),
            item['source'] = 'TheMadkhalis.com - Article - Abu Iyyad',
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item