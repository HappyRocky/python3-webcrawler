# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Question(scrapy.Item):
    id = scrapy.Field()   # 问题id
    title = scrapy.Field() # 问题
    detail = scrapy.Field()  
    excerpt = scrapy.Field()  
    authorId = scrapy.Field()  
    topicsId = scrapy.Field()

class Answer(scrapy.Item):
    id = scrapy.Field()   # 回答id
    questionId = scrapy.Field()  # 问题id
    content = scrapy.Field()  
    excerpt = scrapy.Field()  
    authorId = scrapy.Field()  

class Author(scrapy.Item):
    id = scrapy.Field()   # 用户id
    avatar_url = scrapy.Field()  # 头像
    avatar_url_template = scrapy.Field() # 头像
    headline = scrapy.Field()
    type = scrapy.Field() 
    user_type = scrapy.Field() 
    url_token = scrapy.Field()
    name = scrapy.Field()