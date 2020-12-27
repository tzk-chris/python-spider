import requests
from lxml import etree
import pandas
import os
import re
import pymysql
from threading import Thread


class db:
    ##  连接mysql
    def __init__(self):
        self.conn = pymysql.connect(host='xxx',    #  输入mysql服务器的IP地址
        	user = 'root',                                   #  输入登录用户
        	password = 'xxx',                       #  输入登录密码
        	database = 'xxx',                                #  选择要连接的数据库名
        	charset = 'utf8mb4')                            #   设置好编码，防止后面的操作出现数据类型与编码不吻合
        self.cur = None

    #  设置连接关闭
    def close(self):
        self.conn.close()

    #  设置一个游标
    def cursor(self):
        self.cur = self.conn.cursor()
        return self.cur

    #  设置游标关闭
    def cur_close(self):
        self.cur.close()

    #  设置游标执行sql
    def execute(self, sql):
        if not self.cur:
            self.cursor()
        self.cur.execute(sql)

    #  设置游标的输出
    def cur_print(self):
        self.cur.fetchall()

    #  设置操作事务的提交
    def commit(self):
        self.conn.commit()

#  在这里，获得要爬取的网页的源码
def get_html(url):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}

    try:
        html = requests.get(url, headers=headers)
        html.encoding = html.apparent_encoding
        if html.status_code == 200:
            print("成功获取源代码")
            # print(html.text)
    except Exception as e:
        print("获取源代码失败")

    return html.text

#  在这里开始解析源码，获得数据
def parse_html(html, db):

    html = etree.HTML(html)
    lis = html.xpath("//ol[@class='grid_view']/li")
    imgurls = []

    for li in lis:
        m_name = li.xpath(".//a/span[@class='title']/text()")[0]
        m_persons = pymysql.escape_string(li.xpath(".//div[@class='bd']/p/text()")[0].strip())
        m_info = li.xpath(".//div[@class='bd']/p/text()")[1].strip()
        m_score = int(eval(li.xpath(".//div[@class='star']/span[2]/text()")[0]))
        m_comments = int(re.findall(r"\d+", li.xpath(".//div[@class='star']/span[4]/text()")[0])[0])
        # print(m_comments,type(m_comments))
        try:
            m_introduce = pymysql.escape_string(li.xpath(".//p[@class='quote']/span/text()")[0])
        except Exception as e:
            print(e)
            m_introduce = "none"
        m_imgurl = li.xpath(".//img/@src")[0]
        sql = r"insert into douban(NAME, person, info, score, moment, introduce, poster) VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(m_name, m_persons, m_info, m_score, m_comments, m_introduce, m_imgurl)
        try:
            db.execute(sql)
        except Exception as e:
            print(sql, e)



if __name__ == '__main__':
    db = db()
    for i in range(10):
        url = "https://movie.douban.com/top250?start=" + str(i*25) + '&filter='
        # t1 = Thread(target=get_html, args=(url,))
        html = get_html(url)
        parse_html(html, db)
    db.commit()
    db.cur_close()
    db.close()


# 图片下载：
# def download_img(url,movie):
#     if 'movie_poster' in os.listdir(r'D:\Program Files\我的网站\kun影网'):
#         pass
#     else:
#         os.mkdir('movie_poster')
#     os.chdir(r'D:\Program Files\我的网站\kun影网\movie_poster')
#     print(url)
#     img = requests.get(url).content
#     print(img)
#     with open(movie['name'] + '.jpg',"wb")as f:
#         # print("正在下载:%s"%url)
#         f.write(img)


