from scrapy import Spider
from scrapy.selector import Selector
from data.items import DataItem


class DataSpiderOne(Spider):
    name = "data"

    allowed_domains = [
        "www.shia.bs",
        "www.aboutatheism.net",
        "www.salafis.com",
        "www.theislamblog.com",
        "www.bidah.com",
        "www.asharis.com",
        "www.mutazilah.com",
        "www.islamagainstextremism.com",
        "www.takfiris.com",
        "www.ikhwanis.com",
        "www.barelwis.com",
        "www.nabahani.com",
        "www.islamjesus.ws",
        "www.ibntaymiyyah.com",
        "www.wahhabis.com",
        "www.aqidah.com",
        "www.dajjaal.com",
        "www.abovethethrone.com",
        "www.themadkhalis.com",
        "www.maturidis.com",
        "www.manhaj.com",
    ]

    start_urls = [
        "http://www.shia.bs/authors/Admin.cfm",
        "http://www.shia.bs/authors/Abu.Iyaad.cfm",
        "http://www.shia.bs/authors/Abu.Iyaad.cfm?start=31",
        "http://www.aboutatheism.net/authors/admin.cfm", 
        "http://www.aboutatheism.net/authors/Abu.Iyaad.cfm",
        "http://www.aboutatheism.net/authors/Abu.Iyaad.cfm?start=31",
        "http://www.salafis.com/authors/Abu.Iyaad.cfm",
        "http://www.salafis.com/authors/Abu.Iyaad.cfm?start=31",
        "http://www.theislamblog.com/authors/TheIslamBlog.cfm",
        "http://www.bidah.com/authors/Abu.Iyaad.cfm",
        "https://www.asharis.com/creed/authors/Abu.Iyaad.cfm",
        "https://www.asharis.com/creed/authors/Abu.Iyaad.cfm?start=31",
        "https://www.asharis.com/creed/authors/Abu.Iyaad.cfm?start=61",
        "https://www.asharis.com/creed/authors/Abu.Iyaad.cfm?start=91",
        "https://www.asharis.com/creed/authors/Abu.Iyaad.cfm?start=121",
        "https://www.asharis.com/creed/authors/Abu.Iyaad.cfm?start=151",
        "https://www.asharis.com/creed/authors/Abu.Iyaad.cfm?start=181",
        "https://www.asharis.com/creed/authors/Abu.Iyaad.cfm?start=211",
        "https://www.asharis.com/creed/authors/Abu.Iyaad.cfm?start=241",
        "http://www.mutazilah.com/authors/Abu.Iyaad.cfm",
        "http://www.islamagainstextremism.com/authors/Admin.cfm",
        "http://www.islamagainstextremism.com/authors/Admin.cfm?start=31",
        "http://www.islamagainstextremism.com/authors/Admin.cfm?start=61",
        "http://www.islamagainstextremism.com/authors/Admin.cfm?start=91",
        "https://www.takfiris.com/takfir/categories/articles.cfm",
        "http://www.ikhwanis.com/authors/Abu.Iyaad.cfm",
        "http://www.ikhwanis.com/authors/Abu.Iyaad.cfm?start=31",
        "http://www.barelwis.com/authors/Abu.Iyaad.cfm",
        "http://www.nabahani.com/authors/Abu.Iyaad.cfm",
        "http://www.islamjesus.ws/authors/Abu.Iyaad.cfm",
        "http://www.ibntaymiyyah.com/authors/Abu.Iyaad.cfm",
        "http://www.ibntaymiyyah.com/authors/Abu.Iyaad.cfm?start=31",
        "https://www.aqidah.com/creed/authors/Abu.Iyaad.cfm",
        "https://www.aqidah.com/creed/authors/admin.cfm",
        "https://www.dajjaal.com/liar/authors/Abu.Iyaad.cfm",
        "https://www.dajjaal.com/liar/authors/admin.cfm",
        "https://www.abovethethrone.com/arsh/authors/AboveTheThrone.cfm",
        "https://www.themadkhalis.com/md/authors/Admin.cfm",
        "https://www.maturidis.com/maturidi/authors/Maturidis.Com.cfm",
        "https://www.maturidis.com/maturidi/authors/Admin.cfm",
        "https://www.manhaj.com/manhaj/authors/Abu.Iyaad.cfm",
        "https://www.manhaj.com/manhaj/authors/admin.cfm",
    ]

    def parse(self, response):
        scrapedData = Selector(response).css('a.articleTitleListSmall')

        for data in scrapedData:
            item = DataItem()
            item['title'] = data.css('a.articleTitleListSmall::text').get() + " - Article",
            item['url'] = data.css('a.articleTitleListSmall::attr(href)').get()
            yield item