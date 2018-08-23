#
# https://search.sohu.com/outer/search/meta?keyword=%E4%B8%AD%E6%97%A5&from=20&terminalType=wap&ip=14.16.197.7&city=%E5%B9%BF%E4%B8%9C%E7%9C%81&source=wap-sohu&SUV=1708311245246654&size=10&searchType=news&queryType=edit
#https://search.sohu.com/outer/search/meta?keyword=%E4%B8%AD%E6%97%A5&from=40&terminalType=wap&ip=14.16.197.7&city=%E5%B9%BF%E4%B8%9C%E7%9C%81&source=wap-sohu&SUV=1708311245246654&size=10&searchType=news&queryType=edit
#https://search.sohu.com/outer/search/meta?keyword=%E4%B8%AD%E6%97%A5&from=50&terminalType=wap&ip=14.16.197.7&city=%E5%B9%BF%E4%B8%9C%E7%9C%81&source=wap-sohu&SUV=1708311245246654&size=10&searchType=news&queryType=edit
#https://search.sohu.com/outer/search/meta?keyword=日本&from=20&SUV=1708311245246654
#
import datetime
import re
import time


#from spider_.DBHelper import selectAll, insert
from spider_.common import get_code, get_link, get_content, dict_print, ms2date





def craw_souhu(link_list,keyword="中日"):
    result=[]
    for link in link_list:
        print(link)
        time.sleep(1)
        content=get_content(link,regex_dict={'title':'<meta property="og:title" content="(.*?)"/>',
                                           'pubTime':'<meta property="og:release_date" content="(\d{4}-\d{2}-\d{2} \d{2}:\d{2})"/>',
                                           'content':'<p>(.*?)</p>',
                                             'src':'<meta name="mediaid" content="(.*?)"/>'
                                            })
        content["content"]="".join(re.split(pattern="<.*?>",string=content["content"])).replace("您的浏览器版本过低为了更好的体验，请升级你的浏览器","")
        comment_key="mp_"+str(re.split("/",link)[-1]).split("_")[0]
        comments=get_content("https://apiv2.sohu.com/api/topic/load?page_size=400&topic_source_id=" + comment_key + "&source_id=" + comment_key + "&page_no=1",
                             regex_dict={"comments":'"content":"(.*?)","',
                                         "comTime":'"create_time":(.*?),"'},
                             spliter="#$#")
        # 合并两个字典
        content.update(comments)
        content['link']=link
        # 时间转换
        if len(comments["comTime"])> 1:
            content["comTime"]="#$#".join([ms2date(int(t)) for t in content["comTime"].split("#$#")])
        else:
            print("no comment")

        dict_print(content,mode="short")

        if len(content["content"])>=30 & len(content["title"] )>= 1:
            result.append(content)
    #插入数据库
    print("INSERT#####################################################################################################",end="")
    print(result)
    print("共"+str(len(result))+"篇文章")
    #insert(result,"sohu2",keyword=keyword)
    print("\n\n\n\n\n\n\n")
    time.sleep(3)

if __name__ == '__main__':
    blank=0
    keyword="中日"
    # keyword="中国 日本"
    error_record=[]
    for i in range(0,100):
        page=1
        if i != 0:
            page=i*10
        print("page:",page)

        time.sleep(10)
        try:
            if len(keyword.split(" ")) > 1:
                key="%20".join(keyword.split(" "))
            else:
                key=keyword
            link_list=get_link(url="https://search.sohu.com/outer/search/meta?keyword="+key+"&from="+str(page)+"&SUV=1708311245246654",regex='url":"(http://www\.sohu\.com/a/.*?)"')
            craw_souhu(link_list,keyword=keyword)
        except Exception as err:
            print(err)
            print("ERROR AT "+str(page))
            error_record.append(page)



        if len(link_list) < 2:
            blank=blank+1
        else:
            blank=0

        print("blank:",blank)
        if blank>8:
            break

    print("ERROR:", error_record)