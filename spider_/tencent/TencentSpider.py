import requests
from bs4 import BeautifulSoup
import re


f = open("tencentNews.txt")
#!/usr/bin/env python
# -*- coding: utf-8 -*-
_author_ = 'GavinHsueh'

import requests
import bs4

#要抓取的目标页码地址
url = 'https://new.qq.com/ch/world/'

#抓取页码内容，返回响应对象
response = requests.get(url)

#查看响应状态码
status_code = response.status_code
print(status_code)
#使用BeautifulSoup解析代码,并锁定页码指定标签内容
soup = bs4.BeautifulSoup(response.content.decode("GBK"), "lxml")
# element = content.find_all(id='book')
#
# print(status_code)
# print(element)


# news=soup.find_all('a',href=re.compile('http://news.qq.com/a/20170617/'))
news=soup.find_all('a',href=re.compile('http://new.qq.com/omn/20180820/'))
print(news)
for i in news:
    txt=i.text.strip()
    if txt=='':
        continue
    else:
        u=i.attrs['href']
        ur=requests.get(url=u)
        usoup=BeautifulSoup(ur.text,'lxml')
        f.write(i.text+'\n')
        f.write('正文如下:\n')
        #print(u)
        #print(usoup.body.attrs)
        if usoup.body.attrs['id']=='P-QQ':
            continue
        else:
            p=usoup.find('div',id="content-article").find_all('p')
            for i in p:
                f.write(i.text+'\n')
    f.write('\n')
f.close()
print('finished!')

