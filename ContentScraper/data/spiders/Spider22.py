from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderTwentyTwo(Spider):
    name = "data"

    allowed_domains = [
        "www.salafipubs.com"
    ]

    start_urls = [
        "https://www.salafipubs.com/articles"
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.uk-link-reset')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.uk-link-reset::text').get()
            item['source'] = 'Salafi Publications - Article'
            item['url'] = "https://www.salafipubs.com/" + \
                data.css('a.uk-link-reset::attr(href)').get()
            yield item
