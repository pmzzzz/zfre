# python 3.8
import hmac
import hashlib
import base64
import urllib.parse
import json
from one_process import *
import time
import datetime

ceshi = {

}


# SECf6fe8fa68dda423bb82f81e9c4d44d50301bc7efd3f1203a054bbe9bdb2339de
# https://oapi.dingtalk.com/robot/send?access_token=3108e96a3f90c4309cdc12443e9881d16a9ce9978cfa85c365104d5de84c8b00
# 测试
# def get_url(secret=None, url=None):
#     timestamp = str(round(time.time() * 1000))
#     secret = 'SEC324fa30727ff0505cc3beb25f92fa32e92f58423082f31f7b190c4f9131ed65f'
#     secret_enc = secret.encode('utf-8')
#     string_to_sign = '{}\n{}'.format(timestamp, secret)
#     string_to_sign_enc = string_to_sign.encode('utf-8')
#     hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
#     sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
#     url = 'https://oapi.dingtalk.com/robot/send?access_token=a2b1bb1046f9b876111599ed058dc2f9d1195db270a74fddde49d0b3aebdbaa4'
#     url = url + '&timestamp=' + timestamp + '&sign=' + sign
#     return url


# 业务
def get_url(secret=None, url=None):
    timestamp = str(round(time.time() * 1000))
    secret = secret
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    # url = 'https://oapi.dingtalk.com/robot/send?access_token=de44261bf6286572b28696a704f42b84880cb90a86d46d5271832b175226db34'
    url = url
    url = url + '&timestamp=' + timestamp + '&sign=' + sign
    return url


def send_message(data,url):
    headers = {'Content-Type': 'application/json',
               'charset': 'utf-8'}
    x = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(x.text)


def build_data(raw_data=None, keywords=None):
    if len(raw_data) == 0:
        links = '- 今日无数据\n'
    else:
        names = [i['title'] for i in raw_data]
        hrefs = [i['url'] for i in raw_data]
        links = ''
        i = 1
        for name, href in zip(names, hrefs):
            name = '{}、{}'.format(i, name)
            i += 1
            # one = '- [{}]({})\n'.format(name, href)
            one = '\n{}\n{}\n\n'.format(name, href)
            one = '\n{}\n\n[{}]({})\n\n'.format(name, href, href)
            links += one

    keys = '关键词：' + '/'.join(keywords)
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "今日政策文件如下",
            "text": "## 【今日政策新闻如下】\n> {}\n{}".format(keys, links)
        },
        "at": {
            "isAtAll": True
        }
    }

    return data


def save_json(keywords=None):
    if keywords is None:
        keywords = ['新职业', '补贴', '申报', '认定', '大数据', '人工智能', '区块链', '物联网', '鉴定']
    keywords = keywords
    raw_data = get_all_info_by_day_or_week(mode='day', kw=keywords)
    now = time.strftime('%Y-%m-%d-%H', time.localtime(time.time()))
    js = json.dumps(raw_data)
    fp = './output/{}.json'.format(now)
    with open(fp, 'w', encoding='utf8') as x:
        x.write(js)
    return fp


def getYesterday():
    yesterday = datetime.date.today() + datetime.timedelta(-1)
    return str(yesterday) + '-23'


def test_message():
    keywords = ['新职业', '补贴', '申报', '认定', '大数据', '人工智能', '区块链', '物联网', '鉴定']

    fp = './output/{}.json'.format(getYesterday())
    print(fp)
    fp = './output/2020-12-18-23.json'
    # fp = './output/{}.json'.format('2020-12-28-15')
    with open(fp, 'r') as f:
        content = f.read()
        js = json.loads(content)
    send_message(build_data(raw_data=js, keywords=keywords))
    print('{}发送成功'.format(time_now))


if __name__ == "__main__":
    # test_message()
    keywords = ['新职业', '补贴', '申报', '认定', '大数据', '人工智能', '区块链', '物联网', '鉴定']
    # 输出
    # print(fpo)
    while True:
        time.sleep(1)
        time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新
        print(time_now)
        if time_now == "23:35:00":  # 此处设置每天定时的时间
            # 此处3行替换为需要执行的动作
            # print("hello")
            fp = save_json()
            print('{}保存成功'.format(time_now))
            time.sleep(100)
        if time_now == "08:59:00":
            # print('hello')
            # fp = './output/{}.json'.format(getYesterday())
            print(fp)
            # fp = './output/{}.json'.format('2020-12-28-15')
            with open(fp, 'r') as f:
                content = f.read()
                js = json.loads(content)
            send_message(build_data(raw_data=js, keywords=keywords))
            print('{}发送成功'.format(time_now))
            time.sleep(100)

    # with open(fpo, 'r') as f:
    #     content = f.read()
    #     js= json.loads(content)
    # send_message(build_data(raw_data=js, keywords=keywords))
