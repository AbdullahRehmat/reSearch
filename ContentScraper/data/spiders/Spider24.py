from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class SpiderTwentyFour(Spider):
    name = "data"

    allowed_domains = [
        "www.healthymuslim.com",
    ]

    start_urls = [
        "https://www.healthymuslim.com/authors/abuiyaad.cfm",
        "https://www.healthymuslim.com/authors/Admin.cfm?start=1",
        "https://www.healthymuslim.com/authors/Admin.cfm?start=21",
        "https://www.healthymuslim.com/authors/Admin.cfm?start=41",
        "https://www.healthymuslim.com/authors/Admin.cfm?start=61",
        "https://www.healthymuslim.com/authors/Admin.cfm?start=81",
        "https://www.healthymuslim.com/authors/Admin.cfm?start=101",
        "https://www.healthymuslim.com/authors/Admin.cfm?start=121",
        "https://www.healthymuslim.com/authors/Admin.cfm?start=141",
        "https://www.healthymuslim.com/authors/Admin.cfm?start=161",
        "https://www.healthymuslim.com/authors/Admin.cfm?start=181",
        "https://www.healthymuslim.com/authors/Admin.cfm?start=201",
        "https://www.healthymuslim.com/authors/Admin.cfm?start=221",
        "https://www.healthymuslim.com/authors/Admin.cfm?start=241",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=21",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=41",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=61",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=81",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=101",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=121",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=141",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=161",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=181",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=201",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=221",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=241",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=261",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=281",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=301",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=321",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=341",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=361",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=381",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=401",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=421",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=441",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=461",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=481",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=501",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=521",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=541",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=561",
        "https://www.healthymuslim.com/authors/SoundHealth.cfm?start=581",
        "https://www.healthymuslim.com/authors/HealthyMuslim.cfm",
        "https://www.healthymuslim.com/authors/HealthyMuslim.cfm?start=21",
        "https://www.healthymuslim.com/authors/HealthyMuslim.cfm?start=41",
        "https://www.healthymuslim.com/authors/HealthyMuslim.cfm?start=61",
        "https://www.healthymuslim.com/authors/HealthyMuslim.cfm?start=81",
        "https://www.healthymuslim.com/authors/HealthyMuslim.cfm?start=101",
        "https://www.healthymuslim.com/authors/HealthyMuslim.cfm?start=121",
        "https://www.healthymuslim.com/authors/HealthyMuslim.cfm?start=141",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleLinkOrange')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleLinkOrange::text').get(),
            item['source'] = 'HealthyMuslim.com - Article - Abu Iyyad',
            item['url'] = data.css('a.articleLinkOrange::attr(href)').get()
            yield item
