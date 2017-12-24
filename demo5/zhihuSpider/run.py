from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from zhihuSpider.spiders.QuestionSpider import QuestionSpider
# from zhihuSpider.spiders.ProxiesSpider import ProxiesSpider

process = CrawlerProcess(get_project_settings())  

# process.crawl(ProxiesSpider)
process.crawl(QuestionSpider)  
process.start() # the script will block here until the crawling is finished  