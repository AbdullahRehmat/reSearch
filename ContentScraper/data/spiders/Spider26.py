from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderTwentySix(Spider):
    name = "data"

    allowed_domains = [
        "www.abuiyaad.com",
    ]

    start_urls = [
        "https://www.abuiyaad.com/",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleList')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleList::text').get()
            item['source'] = 'AbuIyaad.com - Article - Abu Iyaad'
            item['url'] = data.css('a.articleTitleList::attr(href)').get()
            yield item
