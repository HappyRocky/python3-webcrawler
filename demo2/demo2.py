#!/usr/bin/python
# -*- coding: UTF-8 -*-

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:      # http异常处理
        return "http异常"

    try:
        bsObj = BeautifulSoup(html.read(), 'lxml')
        title = bsObj.title
    except AttributeError as e:  # 标签异常处理
        return "标签异常"
    return title

title = getTitle('http://www.toutiao.com')
if title == None:
    print ("title 没有找到")
else:
    print(title)