# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os,sys
import sqlite3
from zhihuSpider.items import Question, Answer, Author

class ZhihuspiderWriteToCSVPipeline(object):

    def open_spider(self, spider):
        print("abs path is %s" %(os.path.abspath(sys.argv[0])))
        
        self.csvFile = open(os.path.abspath('../test.csv'), "w+",newline='')
        try:
            self.write = csv.writer(self.csvFile)
            self.write.writerow(('问题id', '问题', '描述', '摘要', '作者Id', '话题id'))
        except Exception as e:
            pass 

    def close_spider(self, spider):
        self.csvFile.close()

    def process_item(self, item, spider):
        try:
            self.write.writerow((item["id"], item["title"], item["detail"], item["excerpt"], item["authorId"], item["topicsId"]))
        except BaseException as e:
            pass
            
        return item

class ZhihuspiderWriteToDBPipeline(object):



    def open_spider(self, spider):
        try:
            self.conn = sqlite3.connect(os.path.abspath('../test.db'))
            self.cursor = self.conn.cursor()
        except BaseException as e:
            pass
            

    def close_spider(self, spider):
        try:
            self.cursor.close()
            self.conn.commit()
            self.conn.close()
        except BaseException as e:
            pass

    def process_item(self, item, spider):
        try:
            if isinstance(item, Question):
                self.cursor.execute('insert into question (id, title, detail, excerpt, authorId, topicsId) values (?, ?, ?, ?, ?, ?)', (item["id"], item["title"], item["detail"], item["excerpt"], item["authorId"], item["topicsId"]))
            if isinstance(item, Answer):
                self.cursor.execute('insert into answer (id, questionId, content, excerpt, authorId) values (?, ?, ?, ?, ?)', (item["id"], item["questionId"], item["content"], item["excerpt"], item["authorId"]))
            if isinstance(item, Author):
                self.cursor.execute('insert into author (id, name, url_token, user_type, type, headline, avatar_url_template, avatar_url) values (?, ?, ?, ?, ?, ?, ?, ?)', (item["id"], item["name"], item["url_token"], item["user_type"], item["type"], item["headline"], item["avatar_url_template"], item["avatar_url"]))
        except BaseException as e:
            print(e)
            pass
            
        return item
