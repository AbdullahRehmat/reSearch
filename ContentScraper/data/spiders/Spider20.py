from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderTwenty(Spider):
    name = "data"

    allowed_domains = [
        "www.maturidis.com",
    ]

    start_urls = [
        "https://www.maturidis.com/maturidi/authors/Maturidis.Com.cfm",
        "https://www.maturidis.com/maturidi/authors/Admin.cfm",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get(),
            item['source'] = 'Maturidis.com - Article - Abu Iyyad',
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item
