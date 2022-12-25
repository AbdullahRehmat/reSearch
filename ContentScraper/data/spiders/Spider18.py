from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderEighteen(Spider):
    name = "data"

    allowed_domains = [
        "www.abovethethrone.com",
    ]

    start_urls = [
        "https://www.abovethethrone.com/arsh/authors/AboveTheThrone.cfm",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get()
            item['source'] = 'AboveTheThrone.com - Article - Abu Iyyad'
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item
