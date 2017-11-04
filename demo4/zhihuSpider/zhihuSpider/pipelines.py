# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os
import sqlite3

class ZhihuspiderWriteToCSVPipeline(object):

    def open_spider(self, spider):
        self.csvFile = open(os.path.abspath('../test.csv'), "w+",newline='')
        try:
            self.write = csv.writer(self.csvFile)
            self.write.writerow(('id', '问题'))
        except Exception as e:
            pass 

    def close_spider(self, spider):
        self.csvFile.close()

    def process_item(self, item, spider):
        try:
            self.write.writerow((item["qId"], item["qTitle"]))
        except BaseException as e:
            pass
            
        return item

class ZhihuspiderWriteToDBPipeline(object):

    def open_spider(self, spider):
        try:
            self.conn = sqlite3.connect(os.path.abspath('../test.db'))
            self.cursor = self.conn.cursor()
            self.cursor.execute('create table question (qId varchar(20) primary key, qTitle varchar(20))')
            conn.commit()
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
            self.cursor.execute('insert into question (qId, qTitle) values (?, ?)', (item["qId"], item["qTitle"]))
        except BaseException as e:
            pass
            
        return item