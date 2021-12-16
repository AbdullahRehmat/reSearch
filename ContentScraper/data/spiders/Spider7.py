from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderSeven(Spider):
    name = "data"

    allowed_domains = [
        "www.mutazilah.com",
    ]

    start_urls = [
        "http://www.mutazilah.com/authors/Abu.Iyaad.cfm",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get(),
            item['source'] = 'Mutazilah.com - Article - Abu Iyyad',
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item
