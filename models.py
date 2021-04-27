import json
import time

from flask_login import UserMixin
from db import Mysql
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from ddddd import get_url, send_message, getYesterday, build_data, save_json
from one_process import *

ON = True
OFF = False
EXC = '意外停止'
urls = {
    '人社': 'http://rlsbj.cq.gov.cn/igs/front/search.jhtml?code=4b5c979955214c8795de1934f5b5a405&timeOrder=desc&siteId'
          '=75&ordryBy=time&position=&pageSize=15',
    '经信委': 'https://jjxxw.cq.gov.cn/igs/front/search.jhtml?code=6f2ae04649c34fa1bdcf611f2e4b5376&timeOrder=desc'
           '&siteId=39&ordryBy=time&position=&pageSize=15',
    '科委': 'http://kjj.cq.gov.cn/igs/front/search.jhtml?code=06ea63ecd64542c7b1ce37f54906a4df&timeOrder=desc&siteId=49'
          '&ordryBy=time&position=&pageSize=15 '
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}

from datetime import datetime
from threading import Timer


# 打印时间函数
def printTime(inc):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    t = Timer(inc, printTime, (inc,))
    t.start()


# 5s
# printTime(5)


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
    def __init__(self, name, url, secret, bot_id, user_id, status=0, kw='大数据', site='人社', period='day',
                 send_time='09:00',
                 create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
        self.result = []
        self.create_time = create_time
        self.status = status
        self.url = url
        self.secret = secret
        self.name = name
        self.id = bot_id
        self.user_id = user_id
        self.period = period
        self.send_time = send_time
        self.kw = kw
        self.site = site

    @classmethod
    def get(cls, bot_id):
        mysql = Mysql()
        id_result = mysql.query_user_id(bot_id)
        if id_result:
            return User(id_result[0], id_result[1], id_result[3], id_result[2])
        else:
            raise RuntimeError('没找到用户')

    # def pa(self):
    #     department = self.site.split('、')
    #     kw = self.kw.split()
    #     mode = self.period
    #     self.result = get_all_info_by_day_or_week(department=department, mode=mode, kw=kw)
    #     if kw == ['，']:
    #         kw = ['无']
    #     print(kw, 'kkkkkkkkwwww')
    #     send_message(data=build_data(raw_data=self.result, keywords=kw), url=get_url(self.secret, self.url))
    #     # print('{}发送成功'.format(time_now))

    def run(self):
        # 发送
        print('run中')
        if self.status == 1:
            # # 修改数据库
            #     tt = self.send_time.split(':')
            #
            #     scheduler = BlockingScheduler()
            #     scheduler.add_job(self.pa, 'cron', hour=tt[0], minute=tt[1])
            # scheduler.start()
            department = self.site.split('、')
            kw = self.kw.split()
            mode = self.period
            self.result = get_all_info_by_day_or_week(department=department, mode=mode, kw=kw)
            if kw == ['，']:
                kw = ['无']
            print(kw, 'kkkkkkkkwwww')
            send_message(data=build_data(raw_data=self.result, keywords=kw), url=get_url(self.secret, self.url))
        # print('{}发送成功'.format(time_now))
        # while self.status == 1:
        #     time.sleep(1)
        #     time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新
        #     print(time_now)
        #     # if time_now == "23:35:00":  # 此处设置每天定时的时间
        #     #     # 此处3行替换为需要执行的动作
        #     #     # print("hello")
        #     #     # fp = save_json()
        #     #     # print('{}保存成功'.format(time_now))
        #     #     # time.sleep(100)
        #     if time_now == self.send_time:
        #         # print('hello')
        #         # fp = './output/{}.json'.format(getYesterday())
        #         # print(fp)
        #         # # fp = './output/{}.json'.format('2020-12-28-15')
        #         # with open(fp, 'r') as f:
        #         #     content = f.read()
        #         #     js = json.loads(content)
        #
        #         time.sleep(100)
        # 停止

    def test(self):
        department = self.site.split()
        kw = self.kw.split()
        mode = 'week'
        kw = self.kw.split()
        test_data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "测试连接",
                "text": "连接成功，请在网页中开启机器人  [去开启](http://127.0.0.1:5000/manage) "
            },
            "at": {
                "isAtAll": False
            }
        }

        x = get_all_info_by_day_or_week(department=department, mode=mode, kw=kw)
        send_message(test_data, url=get_url(self.secret, self.url))
        print('测试', x)

    def close(self):
        self.status = 0
        # 修改数据库
        pass


if __name__ == '__main__':
    url = 'https://oapi.dingtalk.com/robot/send?access_token' \
          '=a2b1bb1046f9b876111599ed058dc2f9d1195db270a74fddde49d0b3aebdbaa4 '
    secret = 'SEC324fa30727ff0505cc3beb25f92fa32e92f58423082f31f7b190c4f9131ed65f'
    bot = Bot(name='人社', url=url, secret=secret, bot_id=1, user_id=100, status=1)
    bot.kw = '，'
    print(bot.run())
