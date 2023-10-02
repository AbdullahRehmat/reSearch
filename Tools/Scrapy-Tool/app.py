import scrapy
from scrapy import Selector
from scrapy.crawler import CrawlerProcess
from spellchecker import SpellChecker


def splitAuthor(scrapedTitle) -> list:
    """ Returns List Containing Title & Authors Name If Present """

    if " By " in scrapedTitle:
        return scrapedTitle.rsplit(" By ", 1)

    else:
        return [scrapedTitle, ""]


class SpiderB(scrapy.Spider):
    name = 'testspider'

    start_urls = ["https://www.salafisounds.com/category/speakers/"]

    def parse(self, response):
        scrapedData = Selector(response).css('h3.mh-posts-grid-title')

        for data in scrapedData:

            scrapedTitle = data.css(
                'h3.mh-posts-grid-title > a::attr(title)').get()

            sc = SpellChecker()
            scrapedTitle = sc.run_spell_checker(scrapedTitle)
            print(scrapedTitle)

            scrapedTitle = splitAuthor(scrapedTitle)
            print(scrapedTitle[0])
            print(scrapedTitle[1])
            print()


if __name__ == "__main__":

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(SpiderB)
    process.start()
