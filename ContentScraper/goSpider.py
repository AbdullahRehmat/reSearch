from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from data.spiders.dataSpiderOne import DataSpiderOne
from data.spiders.dataSpiderTwo import DataSpiderTwo
#from data.spiders.dataSpiderThree import DataSpiderThree

process = CrawlerProcess(get_project_settings())
process.crawl(DataSpiderOne)
process.crawl(DataSpiderTwo)
#process.crawl(DataSpiderThree)
process.start()
