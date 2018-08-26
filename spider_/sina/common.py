import datetime,time
import re
import requests



def get_link(url,regex,encoding='utf-8'):
    """
    通过正则和导航页url获取页面上的连接
    :param url: 导航页url
    :param regex: 正则
    :return: 内容页列表
    """
    code=get_code(url,encoding=encoding)
    url_list=re.findall(regex,code)
    return url_list

def get_content(htmlCode,regex_dict,encoding='utf-8',spliter="\n"):
    """
    通过regex_dict字典中的正则匹配url网页中相应内容
    :param url:
    :param regex_dict:包含正则的字典，字段可以设置多个 （如： {'content':'<p>(.*?)</p>','src':'<meta name="mediaid" content="(.*?)"/>'}）
    :param encoding:
    :return: 采用字典形式返回爬取到的内容
    """
    content_dict={}
    #code=get_code(url,encoding=encoding)
    for key in regex_dict.keys():
        content_dict[key]={}
        content_dict[key]=spliter.join(re.findall(pattern=regex_dict[key],string=htmlCode))
    return content_dict

def get_code(url,encoding='utf-8'):
    """
    获取页面源代码
    :param url:
    :param encoding:
    :return:
    """
    # return requests.get(url).text
    content=requests.get(url).content
    return str(content,encoding)



def dict_print(dic,mode="short"):
    """
    输出字典内容
    :param dic:
    :return:
    """
    print("------")
    for key in dic.keys():
        if mode == "short":
            outprint = dic[key]
            outprint = str(outprint).replace("\n", "")
            if len(outprint) > 100:
                outprint = outprint[:100] + "..."
            print(key + ":", outprint)
        else:
            print(key + ":", dic[key])
    print("------")

def ms2date(ms):
    """
    将毫秒转换成日期格式
    :param ms: 若数字长度大于10 则将从左到右10位以后的移至小数点后
    :return: 日期（如 1534872712859 返回 2018--08--21 17:31  |||   1381419600 返回 2013--10--10 15:40）
    """
    l=len(str(ms))
    t=0
    if l > 10:
        t = l - 10
    ms= ms / (pow(10,t))

    timeStamp = ms
    dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
    otherStyleTime = dateArray.strftime("%Y--%m--%d %H:%M")
    return otherStyleTime



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
        #print(hour)
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


def GetURLGroupByPage(filename):
    """
    :param filename: 存储页面URL的txt文件
    :return:包含新闻标题、URL、时间、来源的字典列表(列表的元素为字典)
    """
    dict_list = []
    with open(filename, "r", encoding="GB18030") as f:
        # page = f.readline()
        page = f.readline()
        i = 1
        while (page):
            time.sleep(3.01)
            htmlCode = get_code(page, encoding="GB18030")  # 获取搜索页面的html代码
            # content = get_content(htmlCode, regex_dict={'link': ''}, encoding="GB18030")

            # 匹配网页源代码需要的正则表达式
            res_div = '<div class="news151102.*?>(.*?)</div>'  # 匹配class为news151102的div,该div中包含title,url,time
            res_title = '<a href=".*?>(.*?)</a>|<a target="_blank" href=".*?>(.*?)</a>'  # 获取a标签里的内容(title)
            res_url = "(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"  # 获取a标签里的url
            res_src = '<p class="news-from">(.*?)&nbsp;.*?</p>'
            res_time = '<p class="news-from">.*?&nbsp;(.*?)<!.*/p>|<p class="news-from">.*?&nbsp;(.*?)</p>'

            div_news151102 = re.findall(res_div, htmlCode, re.S | re.M)
            if len(div_news151102) == 11:
                div_news151102 = div_news151102[0:10]
            else:
                div_news151102 = div_news151102[0:len(div_news151102) - 1]

            for div in div_news151102:  # 一个页面中有多个匹配成功的div
                # print(div)
                content_dict = {}
                title = re.findall(res_title, div, re.I | re.S | re.M)
                if title[0][0] != '':
                    content_dict["title"] = str(title[0][0]) \
                        .replace("<em><!--red_beg-->", '').replace("<!--red_end--></em>", '')
                else:
                    content_dict["title"] = str(title[0][1]) \
                        .replace("<em><!--red_beg-->", '').replace("<!--red_end--></em>", '')
                content_dict["url"] = re.findall(res_url, div, re.I | re.S | re.M)[0]
                content_dict["src"] = re.findall(res_src, div, re.I | re.S | re.M)[0]

                pubTime = re.findall(res_time, div, re.I | re.S | re.M)
                if pubTime[0][0] != '':
                    content_dict["time"] = timeConvert(str(pubTime[0][0]))
                else:
                    content_dict["time"] = timeConvert(str(pubTime[0][1]))
                dict_list.append(content_dict)
                print(content_dict)

            page = f.readline()
            print("以上为第%d页结果" % i,"\n\n")
            i = i + 1
            # print(dict_list[0:2])
    f.close()

    return dict_list

