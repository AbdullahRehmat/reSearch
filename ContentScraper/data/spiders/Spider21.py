from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderTwentyOne(Spider):
    name = "data"

    allowed_domains = [
        "www.manhaj.com",
    ]

    start_urls = [
        "https://www.manhaj.com/manhaj/authors/Abu.Iyaad.cfm",
        "https://www.manhaj.com/manhaj/authors/admin.cfm",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get(),
            item['source'] = 'Manhaj.com - Article - Abu Iyyad',
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item
