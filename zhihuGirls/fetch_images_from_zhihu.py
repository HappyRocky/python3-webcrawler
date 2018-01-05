from selenium import webdriver
import time
import urllib.request
from bs4 import BeautifulSoup
import html.parser

def main():
    # 用火狐浏览器打开知乎网页（前提：将geckodriver.exe放在环境变量下，如C:/Windows）
    driver = webdriver.Firefox()
    #driver.get("https://www.zhihu.com/question/28481779")
    #driver.get("https://www.zhihu.com/question/26037846")
    #driver.get("https://www.zhihu.com/question/36759180")
    #driver.get("https://www.zhihu.com/question/29997789")
    #driver.get("https://www.zhihu.com/question/33554451")
    #driver.get("https://www.zhihu.com/question/32011374")
    driver.get("https://www.zhihu.com/question/38340976")
    
    fileNumber = 6
    
    # 滚动页面到低端，点击查看更多按钮
    def execute_times(times):
        for i in range(times):
            driver.execute_script("window.scroll(0,document.body.scrollHeight);")
            time.sleep(2)
            try:
                driver.find_element_by_css_selector('button.QuestionMainAction').click()
                print("page",str(i))
                time.sleep(1)
            except:
                break
    
    execute_times(200)
    
    result_raw = driver.page_source # 网页源代码
    result_soup = BeautifulSoup(result_raw, 'html.parser')
    result_bf = result_soup.prettify() # 结构化HTML文件
    with open("F:/myPython/images/raw_result.txt", 'w',encoding='utf-8') as girls:
        girls.write(result_bf)
    print("Store raw data successfully")
    
    with open("F:/myPython/images/img_meta.txt",'w',encoding='utf-8') as img_meta:
        noscript_nodes = result_soup.find_all('noscript') # 找到所有<noscript>节点
        noscript_inner_all = ""
        count = 1
        for noscript in noscript_nodes:
            img_url = noscript.find('img').get('src')
            line = str(count) + "\t" + img_url + "\r\n"
            img_meta.write(line)
            urllib.request.urlretrieve(img_url,"F:/myPython/images/images_" + str(fileNumber) + "/" + str(count) + ".jpg") # 下载图片
            count += 1            
    print("Store images successfully,count=",count)
        
if __name__ == '__main__':
    main()