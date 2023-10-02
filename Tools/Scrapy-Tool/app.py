import scrapy
from scrapy import Selector
from scrapy.crawler import CrawlerProcess
from spellchecker import SpellChecker


class TestSpider(scrapy.Spider):
    name = 'testspider'

    start_urls = ["https://www.salafisounds.com/category/speakers/"]

    def parse(self, response):
        scrapedData = Selector(response).css('h3.mh-posts-grid-title')

        for data in scrapedData:
            #title = data.css('h3.mh-posts-grid-title > a::attr(title)').get()
            #url = data.css('h3.mh-posts-grid-title > a::attr(href)').get()

            scrapedTitle = data.css(
                'h3.mh-posts-grid-title > a::attr(title)').get()

            sc = SpellChecker()
            scrapedTitle = sc.run_spell_checker(scrapedTitle)

            if "by " in scrapedTitle:
                title = scrapedTitle.rsplit(" by ", 1)
                print(title[0])
                print(title[1])
                print(title)
                print()

            elif "By " in scrapedTitle:
                title = scrapedTitle.rsplit(" By ", 1)
                print(title[0])
                print(title[1]) 
                print(title)
                print()
            else:
                print(title[0])
                print(title[1]) 
                print()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(TestSpider)
process.start()
