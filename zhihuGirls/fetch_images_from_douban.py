from selenium import webdriver
import time
import urllib.request
from bs4 import BeautifulSoup
import html.parser

def main():
    # 用火狐浏览器打开知乎网页（前提：将geckodriver.exe放在环境变量下，如C:/Windows）
    driver = webdriver.Firefox()
    offset_max = 5
    detail_url_set = set() # 存放详情页面，防止重复
    for i in range(1,offset_max + 1):
        count = 1 # 照片的名称 
        main_url = "https://www.dbmeinv.com/dbgroup/show.htm?cid=7&pager_offset=" + str(i)
        print("Main Page ", i, ": ",main_url)
        driver.get(main_url)
        result_raw = driver.page_source # 网页源代码
        result_soup = BeautifulSoup(result_raw, 'html.parser')
        with open("F:/myPython/images/images_douban/img_meta_" + i + ".txt",'w',encoding='utf-8') as img_meta:
            href_nodes = result_soup.find_all(name='a',attrs={"target":"_topic_detail"}) # 图片a标签
            for href_node in href_nodes:
                detail_url = href_node.get('href') # 点击图片进入的详情页面连接
                if detail_url in detail_url_set: # 链接之前处理过，跳过
                    continue
                detail_url_set.add(detail_url)
                print("  into detail page:", detail_url)
                driver.get(detail_url) # 打开详情页面链接
                detail_raw = driver.page_source
                detail_soup = BeautifulSoup(detail_raw, 'html.parser')
                div_nodes = detail_soup.find_all(name='div',attrs={"class":"topic-figure"}) # 包含图片的div
                for div_node in div_nodes:
                    try:
                        img_node = div_node.select('img[src]')
                        img_src = img_node[0].get('src')
                        line = str(count) + "\t" + img_src + "\r\n"
                        img_meta.write(line)
                        urllib.request.urlretrieve(img_src,"F:/myPython/images/images_douban/" + str(i) + "_" + str(count) + ".jpg") # 下载图片
                        count += 1
                    except:
                        continue
        print("  Store images successfully,count=",count)
        
if __name__ == '__main__':
    main()