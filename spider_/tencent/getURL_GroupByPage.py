from spider_.tencent.common import get_content,get_code
import time

with open("searchEngineURL.txt","r",encoding="GB18030") as f:
    #page = f.readline()
    page = f.readline()
    while(page):
        print(page)
        page = f.readline()
    # print(page)
    #获取搜索引擎的某一页的搜索结果页面后，爬取该页面的每一条新闻的URL
    #getNewsURL(page)
    #htmlCode = get_code(page,encoding="GB18030")
    #content = get_content(htmlCode,regex_dict={'link':''},encoding="GB18030")

f.close()

def timeConvert(gotTime):
    """
    转换时间，e.g.现在是2018-8-24 15:56，爬取的时间为“16小时前”或“57”分钟前，
    则需要将其分别转换成“2018-8-23”和“20818-8-24”

    :param time:爬取的时间，字符型
    :return: 转换后的时间
    """
    currentTime = int(round(time.time() * 1000))    #获取当前毫秒级时间
    if "小时前" in gotTime:
        hour = gotTime.replace("小时前","")
        print(hour)
        hour2ms = int(hour) * 3600000    #1时(h)=3600000毫秒(ms)
        pubTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime((currentTime - hour2ms) / 1000))
        #print(pubTime)
    elif "分钟前" in gotTime:
        minute = gotTime.replace("分钟前","")
        minute2ms = int(minute) * 60000
        pubTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime((currentTime - minute2ms) / 1000))
        #print(pubTime)
    else:
        pubTime = gotTime

    return pubTime[0:10].replace("-0","-")   #搜索引擎的时间戳格式中8月1日显示成8-1而不是08-01


