#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:pmzz
@file:001torch.py
@time:2021/01/19
"""

import pymysql


class Mysql:
    def __init__(self):
        self.content = pymysql.Connect(
            host='121.196.11.83',  # mysql的主机ip
            port=3306,  # 端口
            user='root',  # 用户名
            passwd='ZTzmzyzwanana',  # 数据库密码
            db='zf_crawler',  # 数据库名
            charset='utf8mb4',  # 字符集
        )
        self.cursor = self.content.cursor()

    def add_user(self, name, password, mail):
        sql = 'insert into user (name ,password,mail) values (%s,%s,%s)'
        self.cursor.execute(sql, [name, password, mail])
        self.content.commit()

    def query_all_user(self):
        self.cursor.execute('select * from user')
        return self.cursor.fetchall()

    def query_all_bot(self):
        self.cursor.execute('select * from bot')
        return self.cursor.fetchall()

    def query_mail(self, mail):
        self.cursor.execute('select * from user where mail = %s limit 1 ', [mail])
        return self.cursor.fetchall()
        # self.cursor.execute()

    def query_user_id(self, id):
        self.cursor.execute('select * from user where id = %s limit 1 ', [id])
        return self.cursor.fetchall()

    def add_bot(self, name, url, secret, userID, status,kw='大数据',site=1,period=1,time='09:00'):
        sql = 'insert into bot (name ,url,secret,userID,status,kw,site,period,time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.cursor.execute(sql, [name, url, secret, userID, status,kw,site,period,time])
        self.content.commit()

    def end(self):
        self.cursor.close()
        self.content.close()
######机器人修改

    # def modify_

if __name__ == '__main__':
    mysql = Mysql()
    x = mysql.query_all_user()
    print(x)
    y = mysql.query_mail('123@aa.com')
    print(y)
    # mysql.add_bot('任苏俄', 'www.dsd.com','dadadwffee','100',1)

    z = mysql.query_all_bot()
    print(z)
    a = mysql.query_user_id(1)
    print('xxxxx',a)
    mysql.end()
