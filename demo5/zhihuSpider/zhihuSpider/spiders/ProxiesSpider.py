from scrapy import Spider


class ProxiesSpider(Spider):
    name="proxies"
    allowed_domains = ["zhihu.com"]
    offset = 1
    url = 'http://www.xicidaili.com/nn/%d' % offset
    start_urls = [url]

    def parse(self, response):
        print('ProxiesSpider')