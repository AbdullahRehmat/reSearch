from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderSeventeen(Spider):
    name = "data"

    allowed_domains = [
        "www.dajjaal.com",
    ]

    start_urls = [
        "https://www.dajjaal.com/liar/authors/Abu.Iyaad.cfm",
        "https://www.dajjaal.com/liar/authors/admin.cfm",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get()
            item['source'] = 'Dajjal.com - Article - Abu Iyaad'
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item
