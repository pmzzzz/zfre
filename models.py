import time

from flask_login import UserMixin
from db import Mysql

ON = True
OFF = False
EXC = '意外停止'


class User(UserMixin):
    def __init__(self, user_id, password, mail,name='仙桃'):
        self.id = user_id
        self.password = password
        self.name = name
        self.mail = mail

    @classmethod
    def get(cls, user_id):
        mysql = Mysql()
        id_result = mysql.query_user_id(user_id)
        if id_result:
            return User(id_result[0],id_result[1],id_result[3],id_result[2])
        else:
            raise RuntimeError('没找到用户')

    def get_id(self, ):
        return self.id


class Bot:
    def __init__(self, name, url, secret, botID, status,kw='大数据',site=1,period=1,time='09:00'):
        self.create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.status = EXC
        self.url = url
        self.secret = secret
        self.name = name
        self.id = bot_id
        self.period = period

    pass

if __name__ == '__main__':
    x = User(1,2,3,4)
