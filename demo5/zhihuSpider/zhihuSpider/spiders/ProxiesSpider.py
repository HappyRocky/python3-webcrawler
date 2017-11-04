from scrapy.selector import Selector
from scrapy import Spider
import scrapy
import re
import json

class ProxiesSpider(Spider):
    name="proxies"
    allowed_domains = ["zhihu.com"]
    offset = 1
    url = 'http://www.xicidaili.com/nn/%d' % offset
    start_urls = [url]

    def parse(self, response):
        print('ProxiesSpider')