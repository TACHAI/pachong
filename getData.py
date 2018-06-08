# -*- coding:utf-8 -*
import requests
# 在py3中使用下面的连接包
import pymysql
# import MySQLdb
import os
import threading
from bs4 import BeautifulSoup

# print("连接到mysql...")
# db = MySQLdb.connect("localhost","root","778209","mandc")
# print("连上了")
# cursor = db.cursor()
# # sql = "select * form moveandcsv"
# aa=cursor.execute("select * from moveandcsv")
# print(aa)
# info=cursor.fetchmany(aa)
# for i in info:
#     print(i)
# cursor.close()
# db.close()


def core_code(start,end):
    url = 'http://www.sgs.gov.cn/shaic/'
    # 存到mysql数据库中
    print("连接到mysql...")
    # db = MySQLdb.connect(host="localhost",user="root",passwd="778209",db="mandc",charset="utf8")
    db = pymysql.connect(host="localhost",user="root",passwd="778209",db="mandc",charset="utf8")
    cursor = db.cursor()
    print("连上了")

    # 存到文本中
    # path = os.getcwd()
    # f = open(path + '\\' + '工商回答.txt', 'a', encoding='utf-8')

    for index in range(start,end):
        res = requests.get(url+'consult!getQuestions.action?p='+str(index))
        res.encoding='utf-8'
        soup = BeautifulSoup(res.text,'html.parser')
        # trs=BeautifulSoup(soup)
        # 得到table里面的值
        contxt = soup.select('.list_table')
        for i in contxt:
            temp = 1
            # 遍历里面的tr标签
            while temp < len(i.select('tr')):
                tr = i.select('tr')[temp]
                style = tr.select('td')[0].text
                title = tr.select('td')[1].text
                id = tr.select('td')[1]
                # 得到a标签里面的值
                href = id.select('a')[0].attrs['href']
                # consultant是提问者的名字
                consultant = tr.select('td')[2].text

                ask_time = tr.select('td')[3].text
                statu = tr.select('td')[4].text

                # 点进去里面的值要得到问题内容和答案
                detail = requests.get(url+href)
                detail.encoding = 'utf-8'
                soup1 = BeautifulSoup(detail.text,'html.parser')
                content =soup1.select('table')

                for j in content:
                    temp2 = 0
                    ask_content = j.select('tr')[0].text.strip()
                    reply_content = j.select('tr')[3].text.strip()
                    back_time = j.select('tr')[4].text.strip().split('：')[1]
                    print(style)
                    print(title)
                    print(ask_content)
                    print(reply_content)
                    print(consultant)
                    print(ask_time)
                    print(back_time)
                    # 写到文本中
                    # f.writelines(style)
                    # f.writelines(title)
                    # f.writelines(ask_content)
                    # f.writelines(reply_content)
                    # f.writelines(consultant)
                    # f.writelines(ask_time)
                    # f.writelines(back_time)

                    # 存入到数据库使用dict方式
                    value = {
                        "style": style,
                        "title": title,
                        "ask_content": ask_content,
                        "reply_content": reply_content,
                        "consultant": consultant,
                        "ask_time": ask_time,
                        "back_time": back_time
                    }
                    sql = """insert into gsquestion(style,title,ask_content,reply_content,consultant,ask_time,back_time)
                            VALUES (%(style)s,%(title)s,%(ask_content)s,%(reply_content)s,%(consultant)s,
                            %(ask_time)s,%(back_time)s)"""
                    # "select * from moveandcsv"
                    try:
                        cursor.execute(sql, value)
                        db.commit()
                    except:
                        print("sql插入错误")
                temp += 1
    cursor.close()
    db.close()
# threads = []
#
# t1 = threading.Thread(target=core_code,args=(24,700,))
# t2 = threading.Thread(target=core_code,args=(700,1400,))
# t3 = threading.Thread(target=core_code,args=(1401,2100))
# t4 = threading.Thread(target=core_code,args=(2101,2800))
# t5 = threading.Thread(target=core_code,args=(2801,3500))
# t6 = threading.Thread(target=core_code,args=(3501,4200))
# t7 = threading.Thread(target=core_code,args=(4201,5000))
# t8 = threading.Thread(target=core_code,args=(5001,5700))
# t9 = threading.Thread(target=core_code,args=(5701,6400))
# t10 = threading.Thread(target=core_code,args=(6401,6841))
# threads.append(t1)
# threads.append(t2)
# threads.append(t3)
# threads.append(t4)
# threads.append(t4)
# threads.append(t4)
# threads.append(t4)
threadList=[]
for i in range(1,67):
    threadList.append(threading.Thread(target=core_code, args=(100*i+1,100*(i+1))))


threadList.append(threading.Thread(target=core_code, args=(6801,6841)))
if __name__=='__main__':
    for t in threadList:
        t.setDaemon(True)
        t.start()

while True:
    pass

