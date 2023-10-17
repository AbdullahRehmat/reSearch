from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


def splitAuthor(scrapedTitle) -> list:
    """ Returns List Containing Title & Authors Name If Present """

    if " By " in scrapedTitle:
        return scrapedTitle.rsplit(" By ", 1)

    else:
        return [scrapedTitle, ""]


class SpiderTwentyThree(Spider):
    name = "data"

    allowed_domains = [
        "www.salafisounds.com"
    ]

    def gen_start_urls(url, number):
        """ Generated A List Of Start URLS """
        i = 0
        start_urls = []

        while i <= number:
            start_urls.append(str(url) + str(i))
            i += 1

        return start_urls

    start_urls = gen_start_urls(
        "https://www.salafisounds.com/category/speakers/page/", 200)

    print(start_urls)

    def parse(self, response):
        scrapedData = Selector(response).css('h3.mh-posts-grid-title')

        for data in scrapedData:
            item = DataItem()

            scrapedTitle = data.css(
                'h3.mh-posts-grid-title > a::attr(title)').get()

            # Remove Author / Speaker From Title & Append To Source
            title = splitAuthor(scrapedTitle)
            item['title'] = title[0]
            item['source'] = 'Salafi Sounds - Audio - ' + title[1]
            item['url'] = data.css(
                'h3.mh-posts-grid-title > a::attr(href)').get()

            yield item