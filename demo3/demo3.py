#!/usr/bin/python
# -*- coding: UTF-8 -*-

from urllib.request import urlopen

from bs4 import BeautifulSoup

html = urlopen("https://www.zhihu.com/explore")
bsObj = BeautifulSoup(html, 'lxml')
bsList = bsObj.findAll("", {"class":"explore-feed feed-item"})
for bsItem in bsList:
  qsLink = bsItem.find("a",{"class":"question_link"})
  author = bsItem.find("span", {"class": "author-link-line"})
  vote = bsItem.find("div",{"class": "zm-item-vote"})
  print(" 标题: %s\n 地址：%s\n 回答者：%s \n 点赞数：%s \n" % (qsLink.get_text().strip(), qsLink.attrs["href"], author.get_text().strip(), vote.get_text().strip()))