from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from data.spiders.dataSpider import DataSpider

process = CrawlerProcess(get_project_settings())
process.crawl(DataSpider)
process.start()
