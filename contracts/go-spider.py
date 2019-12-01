from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.get_contracts import GetContractsSpider

process = CrawlerProcess(get_project_settings())
process.crawl(GetContractsSpider)
process.start()