from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderTwo(Spider):
    name = "data"

    allowed_domains = [
        "www.aboutatheism.net",
    ]

    start_urls = [
        "http://www.aboutatheism.net/authors/admin.cfm",
        "http://www.aboutatheism.net/authors/Abu.Iyaad.cfm",
        "http://www.aboutatheism.net/authors/Abu.Iyaad.cfm?start=31",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get(),
            item['source'] = 'AboutAtheism.net - Article - Abu Iyyad',
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item
