import re

import scrapy
from scrapy import Spider
from zhihuSpider.items import Question


class QuestionSpider(Spider):
    name="question"
    allowed_domains = ["zhihu.com"]
    offset = 5
    url = 'https://www.zhihu.com/node/ExploreAnswerListV2?params={"offset": %d, "type": "day"}' % offset
    start_urls = [url]

    def parse(self, response):
        item = Question()
        res = response.css("a.question_link")  # 获取所有问题节点，后续处理
        for q in res:
            # 处理请求内容
            link = q.css("::attr(href)").extract_first().strip()    # 获取链接
            m = re.match(r"/question/(\d+)/answer/\d+", link)       # 正则匹配获取问题id
            if m:
                qId = m.group(1)
            else:
                qId = '0000'

            question = q.css("::text").extract_first().strip()      # 获取问题标题

            item['qId'] = qId
            item['qTitle'] = question
            print("qid: %s" % qId)
            yield item
        
        if len(res) >= 5:
            # 请求下一页数据
            QuestionSpider.offset += 5
            yield scrapy.Request('https://www.zhihu.com/node/ExploreAnswerListV2?params={"offset": %d, "type": "day"}' % QuestionSpider.offset, callback=self.parse)