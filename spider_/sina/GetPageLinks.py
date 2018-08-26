import re,time,random
from spider_.sina.common import get_code,timeConvert

def GetURLGroupByPage(url):
    """
    :param filename: 存储页面URL的txt文件
    :return:包含新闻标题、URL、时间、来源的字典列表(列表的元素为字典)
    """
    dict_list = []

    i = 1

    time.sleep(random.uniform(2.9, 4.1))
    htmlCode = get_code(url, encoding="GB18030")  # 获取搜索页面的html代码

    # 匹配网页源代码需要的正则表达式
    res_div = '<div class="box-result clearfix".*?>(.*?)</div>'  # 匹配class为box-result clearfix,该div中包含title,url,time
    res_title = '<a href=".*?>(.*?)</a>'  # 获取a标签里的内容(title)
    res_url = "(?<=<a href=\").+?(?=\")"  # 获取a标签里的url
    res_src_and_time = '<span class="fgray_time">(.*?)</span>'  # 获取span标签里的新闻来源和时间

    divs = re.findall(res_div, htmlCode, re.S | re.M)
    if len(divs) == 20:
        divs = divs[0:20]
    else:
        divs = divs[0:len(divs) - 1]

    for div in divs:  # 一个页面中有多个匹配成功的div
        content_dict = {}
        title = re.findall(res_title, div, re.I | re.S | re.M)[0]
        title = str(title).replace("<span style=\"color:#C03\">", "").replace("</span>", "")
        content_dict["title"] = title
        content_dict["url"] = re.findall(res_url, div, re.I | re.S | re.M)[0]
        src_and_time = re.findall(res_src_and_time, div, re.I | re.S | re.M)[0]
        content_dict["src"] = str(src_and_time).split(" ")[0]
        content_dict["time"] = str(src_and_time).split(" ")[1] + " " + str(src_and_time).split(" ")[2]
        dict_list.append(content_dict)
        #print(content_dict["time"])

    print("以上为第%d页结果" % i, "\n\n")
    i = i + 1


    return dict_list

# a = GetURLGroupByPage("https://search.sina.com.cn/?q=%D6%D0%C8%D5&range=title&c=news&sort=time&col=&source=&from=&country=&size=&time=&a=&page=1&pf=2131425516&ps=2132736812&dpc=1")
# print(a)

def URLGenerator(pageNum):
    """
    因为URL中包含%D等字符，无法使用格式化输入，一时之间也想不到更好的解决方法，所以定义了一个方法来生成URL
    :param pageNum: 数值型
    :return: 完整的URL，字符型
    """
    url = 'https://search.sina.com.cn/?q=%D6%D0%C8%D5&range=title&c=news&sort=time&col=&source=&' \
         'from=&country=&size=&time=&a=&page=' + str(pageNum) + '%s&pf=2131425516&ps=2132736812&dpc=1'
    return url
