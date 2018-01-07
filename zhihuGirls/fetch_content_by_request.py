from urllib import parse,request
import json
import http.cookiejar

min_time = "1515344712"
img_path = "F:/myPython/images/images_neihanduanzi/"
referer = "http://m.neihanshequ.com/category/109/"
header = {
"Accept":"*/*",
# "Accept-Encoding":"gzip, deflate, sdch",
"Accept-Language":"zh-CN,zh;q=0.8",
"Connection":"keep-alive",
"Referer":referer,
"X-Requested-With":"XMLHttpRequest",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
}
cj = http.cookiejar.CookieJar()
opener = request.build_opener(request.HTTPCookieProcessor(cj))
img_name_set = set() # 存放名称，防止重复
for i in range(10):
    print('request ',i)
    url = referer + "?is_json=1&app_name=neihanshequ_web&min_time=" + min_time + "&csrfmiddlewaretoken=5e957b257802bb515f9ff7ca07d51c89"
    req = request.Request(url=url,headers=header)
    # res = request.urlopen(req) # 这样不会带cookie
    res = opener.open(req)
    res = res.read()
    try:
        res = res.decode(encoding='utf-8')
    except:
        print("res=",res)
    res_json = json.loads(res)
    min_time = str(res_json['data']['min_time'])
    list = res_json['data']['data']
    for item in list:
        group = item['group']
        if 'large_image' in group.keys():
            url_list = group['large_image']['url_list']
            for img_url_dic in url_list:
                img_url = img_url_dic['url']
                img_name_idx = img_url.rfind('/')
                if(img_name_idx >= 0):    
                    img_name = img_url[(img_name_idx + 1):]
                    if img_name in img_name_set:
                        continue
                    try:
                        request.urlretrieve(img_url, img_path + img_name + ".jpg") # 下载图片
                    except:
                        continue
                    else:
                        img_name_set.add(img_name)
                        print('success downloading img:',img_url)                        
                        break
                    