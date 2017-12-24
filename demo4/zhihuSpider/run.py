from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from zhihuSpider.spiders.QuestionSpider import QuestionSpider

process = CrawlerProcess(get_project_settings())  

process.crawl(QuestionSpider)  
process.start() 