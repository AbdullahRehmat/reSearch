from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from data.spiders.Spider1 import SpiderOne
from data.spiders.Spider2 import SpiderTwo
from data.spiders.Spider3 import SpiderThree
from data.spiders.Spider4 import SpiderFour
from data.spiders.Spider5 import SpiderFive
from data.spiders.Spider6 import SpiderSix
from data.spiders.Spider7 import SpiderSeven
from data.spiders.Spider8 import SpiderEight
from data.spiders.Spider9 import SpiderNine
from data.spiders.Spider10 import SpiderTen
from data.spiders.Spider11 import SpiderEleven
from data.spiders.Spider12 import SpiderTwelve
from data.spiders.Spider13 import SpiderThirteen
from data.spiders.Spider14 import SpiderFourteen
from data.spiders.Spider15 import SpiderFifteen
from data.spiders.Spider16 import SpiderSixteen
from data.spiders.Spider17 import SpiderSeventeen
from data.spiders.Spider18 import SpiderEighteen
from data.spiders.Spider19 import SpiderNineteen
from data.spiders.Spider20 import SpiderTwenty
from data.spiders.Spider21 import SpiderTwentyOne
from data.spiders.Spider22 import SpiderTwentyTwo
from data.spiders.Spider23 import SpiderTwentyThree
from data.spiders.Spider24 import SpiderTwentyFour


process = CrawlerProcess(get_project_settings())

process.crawl(SpiderOne)
process.crawl(SpiderTwo)
process.crawl(SpiderThree)
process.crawl(SpiderFour)
process.crawl(SpiderFive)
process.crawl(SpiderSix)
process.crawl(SpiderSeven)
process.crawl(SpiderEight)
process.crawl(SpiderNine)
process.crawl(SpiderTen)
process.crawl(SpiderEleven)
process.crawl(SpiderTwelve)
process.crawl(SpiderThirteen)
process.crawl(SpiderFourteen)
process.crawl(SpiderFifteen)
process.crawl(SpiderSixteen)
process.crawl(SpiderSeventeen)
process.crawl(SpiderEighteen)
process.crawl(SpiderNineteen)
process.crawl(SpiderTwenty)
process.crawl(SpiderTwentyOne)
process.crawl(SpiderTwentyTwo)
process.crawl(SpiderTwentyThree)
process.crawl(SpiderTwentyFour)

process.start()
