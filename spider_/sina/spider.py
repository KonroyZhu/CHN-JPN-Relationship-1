from spider_.sina.GetPageLinks import URLGenerator,GetURLGroupByPage
from spider_.DBHelper import operate_with_sql
import requests

if __name__ == '__main__':
    pageNum = 1
    newsCount =1
    # print(requests.get(URLGenerator(pageNum)).status_code)
    # print(type(requests.get(URLGenerator(pageNum)).status_code))
    while(requests.get(URLGenerator(pageNum)).status_code == 200):
        dict_list = GetURLGroupByPage(URLGenerator(pageNum))
        sql = "insert into sinalink (title,newsTime,link,src) VALUES (%s,%s,%s,%s)"
        i = 1
        for dic in dict_list:
            print(dic)
            sql = "insert into sinalink (title,newsTime,link,src) VALUES ('%s','%s','%s','%s')" % (dic["title"], dic["time"], dic["url"], dic["src"])
            #print(sql)
            operate_with_sql(sql)
            print("第%d条新闻插入数据库成功！" %newsCount, "\n")
            newsCount += 1
        pageNum += 1

