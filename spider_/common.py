import datetime
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

def get_content(url,regex_dict,encoding='utf-8',spliter="\n"):
    """
    通过regex_dict字典中的正则匹配url网页中相应内容
    :param url:
    :param regex_dict:包含正则的字典，字段可以设置多个 （如： {'content':'<p>(.*?)</p>','src':'<meta name="mediaid" content="(.*?)"/>'}）
    :param encoding:
    :return: 采用字典形式返回爬取到的内容
    """
    content_dict={}
    code=get_code(url,encoding=encoding)
    for key in regex_dict.keys():
        content_dict[key]={}
        content_dict[key]=spliter.join(re.findall(pattern=regex_dict[key],string=code))
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

def test():
    print("this is a test.")