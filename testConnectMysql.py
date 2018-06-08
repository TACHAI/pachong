# -*- coding:utf-8 -*
import MySQLdb

print("连接到mysql...")
db = MySQLdb.connect(host="localhost",user="root",passwd="778209",db="mandc",charset="utf8")
print("连上了")
cursor = db.cursor()
style="内资"
value={
"style":style,
"title":'公司地址变更，',
"ask_content":'公司名称变更和企业法人,可以一起办理吗？',
"reply_content":'建议和迁入地和迁出地咨询一下',
"consultant":'孙大成',
"ask_time":'2018-05-08 16:20',
"back_time":'2018-05-08 16:41'
}


# ask_time='2018-05-08 16:20'
# back_time='2018-05-08 16:41'
sql= """insert into gsquestion(style,title,ask_content,reply_content,consultant,ask_time,back_time)
        VALUES (%(style)s,%(title)s,%(ask_content)s,%(reply_content)s,%(consultant)s,
        %(ask_time)s,%(back_time)s)"""
#"select * from moveandcsv"
cursor.execute(sql,value)
db.commit()
cursor.close()
db.close()
