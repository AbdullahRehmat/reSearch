from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderSix(Spider):
    name = "data"

    allowed_domains = [
        "www.asharis.com",
    ]

    start_urls = [
        "https://www.asharis.com/creed/authors/Abu.Iyaad.cfm",
        "https://www.asharis.com/creed/authors/Abu.Iyaad.cfm?start=31",
        "https://www.asharis.com/creed/authors/Abu.Iyaad.cfm?start=61",
        "https://www.asharis.com/creed/authors/Abu.Iyaad.cfm?start=91",
        "https://www.asharis.com/creed/authors/Abu.Iyaad.cfm?start=121",
        "https://www.asharis.com/creed/authors/Abu.Iyaad.cfm?start=151",
        "https://www.asharis.com/creed/authors/Abu.Iyaad.cfm?start=181",
        "https://www.asharis.com/creed/authors/Abu.Iyaad.cfm?start=211",
        "https://www.asharis.com/creed/authors/Abu.Iyaad.cfm?start=241",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get()
            item['source'] = 'Asharis.com - Article - Abu Iyyad'
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item
