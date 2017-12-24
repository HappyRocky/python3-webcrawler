import json
import re

import scrapy
from scrapy import Spider
from zhihuSpider.items import Question, Answer, Author


class QuestionSpider(Spider):
    name="question"
    allowed_domains = ["zhihu.com"]
    QuestionIds = []
    AnswerIds = []
    AuthorIds = []


    answer_params = "include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,upvoted_followees;data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].topics&sort_by=default"

    def start_requests(self):
        yield scrapy.Request('https://www.zhihu.com/node/ExploreAnswerListV2?params={"offset": 0, "type": "day"}' , callback=self.parse,meta={"offset":0, "type": "day"}, headers={"authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"})
        yield scrapy.Request('https://www.zhihu.com/node/ExploreAnswerListV2?params={"offset": 0, "type": "month"}' , callback=self.parse,meta={"offset":0, "type": "month"}, headers={"authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"})

    # 处理相似问题
    def processSimilarQuestions (self, response):
        print ("processSimilarQuestions ============== ")
        body = json.loads(response.body)
        for q in body["data"]:
            if q["id"] in self.QuestionIds:
                continue
            yield scrapy.Request('https://www.zhihu.com/question/%s' % q["id"], callback=self.parse, meta={"qId":q["id"]}, headers={"authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"})

        if body["paging"]["is_end"] == False:
            yield scrapy.Request(body["paging"]["next"], callback=self.processSimilarQuestions, headers={"authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"})
        
        if body["paging"]["is_start"] == False:
            yield scrapy.Request(body["paging"]["previous"], callback=self.processSimilarQuestions, headers={"authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"})

    # 处理问题
    def processingQuestion (self, response):
        item = Question()
        item1 = Author()
        data = json.loads(response.css("#data::attr(data-state)").extract_first())
        question = data["entities"]["questions"]
        for qId in question:
            if qId in self.QuestionIds:
                print ("pass QuestionIds: %s" % qId)
                continue
            self.QuestionIds.append(qId)
            item["id"] = qId
            item["title"] = question[qId]["title"]
            item["detail"] = question[qId]["detail"]
            item["excerpt"] = question[qId]["excerpt"]
            item["authorId"] = question[qId]["author"]["id"]
            topics = []
            for topic in question[qId]["topics"]:
                topics.append(topic["id"])
            item["topicsId"] = ",".join(topics)

            if question[qId]["author"]["id"] in self.AuthorIds:
                print ("pass AuthorIds: %s" % question[qId]["author"]["id"])
                continue
            self.AuthorIds.append(question[qId]["author"]["id"])
            print("用户ID: %s" % question[qId]["author"]["id"])
            item1["id"] = question[qId]["author"]["id"]   # 用户id
            item1["avatar_url"] = question[qId]["author"]["avatarUrl"]  # 头像
            item1["avatar_url_template"] = question[qId]["author"]["avatarUrlTemplate"] # 头像
            item1["headline"] = question[qId]["author"]["headline"]
            item1["type"] = question[qId]["author"]["type"] 
            item1["user_type"] = question[qId]["author"]["userType"] 
            item1["url_token"] = question[qId]["author"]["urlToken"]
            item1["name"] = question[qId]["author"]["name"]
            yield item
            yield item1

    # 处理回答
    def parseAnswerDatas (self, response):
        item = Answer()
        item1 = Author()
        body = json.loads(response.body)
        qId = response.meta["qId"]
                
        for answer in body["data"]:
            if answer["id"] in self.AnswerIds:
                print ("pass AnswerIds: %s" % answer["id"])
                continue
            self.AnswerIds.append(answer["id"])
            print("回答ID: %s" % answer["id"])
            item["id"] = answer["id"]   # 回答id
            item["questionId"] = qId  # 问题id
            item["content"] = answer["content"]  
            item["excerpt"] = answer["excerpt"] 
            item["authorId"] = answer["author"]["id"]

            if answer["author"]["id"] in self.AuthorIds:
                print ("pass AuthorIds: %s" % answer["author"]["id"])
                continue
            self.AuthorIds.append(answer["author"]["id"])
            print("用户ID: %s" % answer["author"]["id"])
            item1["id"] = answer["author"]["id"]   # 用户id
            item1["avatar_url"] = answer["author"]["avatar_url"]  # 头像
            item1["avatar_url_template"] = answer["author"]["avatar_url_template"] # 头像
            item1["headline"] = answer["author"]["headline"]
            item1["type"] = answer["author"]["type"] 
            item1["user_type"] = answer["author"]["user_type"] 
            item1["url_token"] = answer["author"]["url_token"]
            item1["name"] = answer["author"]["name"]
            yield item
            yield item1

        if body["paging"]["is_end"] == False:
            yield scrapy.Request('https://www.zhihu.com/api/v4/questions/%s/answers?offset=1&limit=20&%s' % (qId, self.answer_params), callback=self.parseAnswerDatas, headers={"authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"}, meta={"qId":qId, "offset": response.meta["offset"] + 20, "limit": 20})

    def parse(self, response):
        res = response.css("a.question_link")  # 获取所有问题节点，后续处理
        for q in res:
            # 请求问题内容
            link = q.css("::attr(href)").extract_first().strip()    # 获取链接
            m = re.match(r"/question/(\d+)/answer/\d+", link)       # 正则匹配获取问题id
            qId = m.group(1)
            print("问题ID: %s" % qId)
            yield scrapy.Request('https://www.zhihu.com/question/%s' % qId, callback=self.processingQuestion, meta={"qId":qId}, headers={"authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"})
            yield scrapy.Request('https://www.zhihu.com/api/v4/questions/%s/answers?offset=1&limit=20&%s' % (qId, self.answer_params), callback=self.parseAnswerDatas, headers={"authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"},meta={"qId":qId, "offset": 1, "limit": 20})
            yield scrapy.Request("https://www.zhihu.com/api/v4/questions/%s/similar-questions?include=data[*].answer_count,author,follower_count&limit=5&offset=0" %qId, callback=self.processSimilarQuestions, headers={"authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"})
            
        
        if len(res) >= 5:
            # 请求下一页数据
            yield scrapy.Request('https://www.zhihu.com/node/ExploreAnswerListV2?params={"offset": %d, "type": "%s"}' % (response.meta["offset"],response.meta["type"]), callback=self.parse,meta={"offset":response.meta["offset"] + 5}, headers={"authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"})