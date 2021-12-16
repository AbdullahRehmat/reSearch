from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderFour(Spider):
    name = "data"

    allowed_domains = [
        "www.theislamblog.com",
    ]

    start_urls = [
        "http://www.theislamblog.com/authors/TheIslamBlog.cfm",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get(),
            item['source'] = 'TheIslamBlog.com - Article - Abu Iyyad',
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item
