import time

from flask_login import UserMixin
from db import Mysql

ON = True
OFF = False
EXC = '意外停止'


class User(UserMixin):
    def __init__(self, user_id, password, mail, name='仙桃'):
        self.id = user_id
        self.password = password
        self.name = name
        self.mail = mail

    @classmethod
    def get(cls, user_id):
        mysql = Mysql()
        id_result = mysql.query_user_id(user_id)[0]
        print('id_result', id_result)
        if id_result:
            return User(user_id=id_result[0], name=id_result[1], password=id_result[2], mail=id_result[3])
        else:
            # raise RuntimeError('没找到用户')
            return None


class Bot:
    # name, url, secret, userID, status, kw, site, period, time
    def __init__(self, name, url, secret, bot_id, user_id, status, kw='大数据', site='人设', period=1, send_time='09:00',
                 create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
        self.create_time = create_time
        self.status = EXC
        self.url = url
        self.secret = secret
        self.name = name
        self.id = bot_id
        self.user_id = user_id
        self.period = period
        self.send_time = send_time

    @classmethod
    def get(cls, bot_id):
        mysql = Mysql()
        id_result = mysql.query_user_id(bot_id)
        if id_result:
            return User(id_result[0], id_result[1], id_result[3], id_result[2])
        else:
            raise RuntimeError('没找到用户')

    pass


if __name__ == '__main__':
    x = User(1, 2, 3, 4)
