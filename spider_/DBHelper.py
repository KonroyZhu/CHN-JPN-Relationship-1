import pymysql



def insert(newsList,tableName,keyword):
    """
    :param newsList: 用来存放新闻的列表，列表包含若干个字典，每个字典中含有以下的key：
    title:文章的标题
    pubTime:文章的发布时间
    src：来源，e.g.广州日报，大洋网
    content:文章正文
    comments:评论
    comTime：评论时间
    link:新闻对应的链接

    :param tableName:不同的新闻网站对应不同的表
    :param keyword:字符型，用于检索的关键字，如“中日”，“日本”等
    """

    # 数据库连接字符串
    conn = pymysql.connect(host='YOUR MYSQL HOSTNAME',
                                 port=3306,
                                 user='YOUR MYSQL USERNAME',
                                 password='YOUR MYSQL USER PASSWORD',
                                 db='YOUR MYSQL DATABASE NAME',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()    #通过cursor创建游标
    # insertSQL = "insert into" + str(tableName) + "(title,pubTime,src,content,comments,comTime) VALUES('%s')"
    insertSQL = "insert into " + tableName + " (title,pubTime,src,content,comments,comTime,keyword,link) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    print(insertSQL)

    for dict in newsList:
        cursor.execute(insertSQL ,(dict['title'], dict['pubTime'],
                                    dict['src'], dict['content'], dict['comments'], dict['comTime'],dict['link'],keyword))
        conn.commit()#提交
    cursor.close()
    conn.close()


# insert([{'title':'标题','pubTime':'2018-8-21 21:00','src':'大洋网','content':'这是正文',
#             'comments':'这是评论','comTime':'2018-8-31 20:00','link':'www.baidu.com'}],"sohu")
# insert([{'title':'标题','pubTime':'2018-8-21 21:00','src':'大洋网','content':'这是正文',
#             'comments':'这是评论','comTime':'2018-8-31 20:00'}],"sohu")


def operate_with_sql(sql):
    """
    :param sql:执行指定的sql语句(没有返回值的操作)
    :return:
    """

    # 数据库连接字符串
    conn = pymysql.connect(host='YOUR MYSQL HOSTNAME',
                                 port=3306,
                                 user='YOUR MYSQL USERNAME',
                                 password='YOUR MYSQL USER PASSWORD',
                                 db='YOUR MYSQL DATABASE NAME',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()    #通过cursor创建游标

    try:
        cursor.execute(sql)
        conn.commit()#提交
    except Exception as ex:
        print(ex)
    finally:
        cursor.close()
        conn.close()



def selectAll(tableName):
    """
    :param tableName:  要遍历的表名
    :return: 查询的结果 -> dict
    """

    conn = pymysql.connect(host='YOUR MYSQL HOSTNAME',
                                 port=3306,
                                 user='YOUR MYSQL USERNAME',
                                 password='YOUR MYSQL USER PASSWORD',
                                 db='YOUR MYSQL DATABASE NAME',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()  # 通过cursor创建游标

    selectAllSQL = "select * from " + tableName
    cursor.execute(selectAllSQL)

    result = cursor.fetchall()    #获取查询结果的所有行
    #result = cursor.fetchone()    #获取查询结果的第一行
    #result = cursor.fetchmany(3)    #获取查询结果的前n行，此处n = 3

    for dict in result:
        print(dict)
    cursor.close()
    conn.close()

    #selectAll("sohu")





