from spider_.tencent.common import GetURLGroupByPage
from spider_.DBHelper import operate_with_sql

if __name__ == '__main__':
    dict_list = GetURLGroupByPage("searchEngineURL.txt")
    sql = "insert into tencentlink (title,newsTime,link,src) VALUES (%s,%s,%s,%s)"
    i = 1
    for dic in dict_list:
        print(dic,"\n")
        sql = "insert into tencentlink (title,newsTime,link,src) VALUES ('%s','%s','%s','%s')" % (dic["title"], dic["time"], dic["url"], dic["src"])
        #print(sql)
        operate_with_sql(sql)
        print("第%d条新闻插入数据库成功！" %i, "\n")
        i += 1

