from urllib.request import urlopen

html = urlopen("http://www.toutiao.com/")

print(html.read())