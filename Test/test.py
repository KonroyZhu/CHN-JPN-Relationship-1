#http://news.sogou.com/news?mode=2&manual=true&query=site%3Aqq.com+%D6%D0%C8%D5&sort=1&page=1&p=42230302&dp=1
#http://news.sogou.com/news?mode=2&manual=true&query=site%3Aqq.com+%D6%D0%C8%D5&sort=1&page=2&p=42230302&dp=1
#http://news.sogou.com/news?mode=2&manual=true&query=site%3Aqq.com+%D6%D0%C8%D5&sort=1&page=3&p=42230302&dp=1

#按页面保存搜索结果链接
# with open("searchEngineURL.txt","w",encoding="utf-8") as f:
#     i = 1
#     for i in range(1,38):
#         f.write("http://news.sogou.com/news?mode=2&manual=true&query=site%3Aqq.com+%D6%D0%C8%D5&sort=1&page=")
#         f.write(str(i))
#         f.write("&p=42230302&dp=1\n")
#         i += 1
# f.close()

import re
from spider_.common import get_code
code = get_code("http://news.sogou.com/news?mode=2&manual=true&query=site%3Aqq.com+%D6%D0%C8%D5&sort=1&page=1&p=42230302&dp=1",encoding="GB18030")
res_div = '<div class="news151102.*?>(.*?)</div>'
res_a = '<a href=".*?>(.*?)</a>|<a target="_blank" href=".*?>(.*?)</a>'#获取a标签里的内容(title)
res_url = "(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
res_src = '<p class="news-from">(.*?)&nbsp;.*?</p>'
res_time = '<p class="news-from">.*?&nbsp;(.*?)<!.*/p>'

#<p class="news-from">腾讯科技&nbsp;10小时前<!--resultinfodate:10小时前--></p>
#<div class="news151102"></div>
urls=re.findall("<a.*?href=.*?<\/a>", code, re.I|re.S|re.M)#完整的<a></a>
div_news151102 =  re.findall(res_div, code, re.S|re.M)[0]
a =  re.findall(res_a, div_news151102, re.I|re.S|re.M)[0][0]
url = re.findall(res_url,div_news151102,re.I|re.S|re.M)[0]
src = re.findall(res_src,div_news151102,re.I|re.S|re.M)[0]
time = re.findall(res_time,div_news151102,re.I|re.S|re.M)[0]
# for value in div_news151102:
#     print (value)
#print(div_news151102)
print(a)
#print(a)
#print(url)

