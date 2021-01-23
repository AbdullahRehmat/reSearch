from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class DataSpider(Spider):
    name = "data"

    allowed_domains = ["aboutatheism.net"]

    start_urls = [
        "http://www.aboutatheism.net/archives/2018/12/index.cfm",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get(),
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item
