from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderSixteen(Spider):
    name = "data"

    allowed_domains = [
        "www.aqidah.com",
    ]

    start_urls = [
        "https://www.aqidah.com/creed/authors/Abu.Iyaad.cfm",
        "https://www.aqidah.com/creed/authors/admin.cfm",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get()
            item['source'] = 'Aqidah.com - Article - Abu Iyyad'
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item
