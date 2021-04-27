import json
import time
import one_process
import ddddd


def build_tody_all(raw_data=None, keywords=None):
    names = [i['title'] for i in raw_data]
    hrefs = [i['url'] for i in raw_data]
    links = ''
    for name, href in zip(names, hrefs):
        one = '- [{}]({})\n'.format(name, href)
        links += one

    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "今日政策文件如下",
            "text": "# 今日政策新闻如下：\n{}".format(links)
        },
        "at": {
            "isAtAll": True
        }
    }

    return data


def get_text(department, raw_data):
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
            one = '- [{}]({})\n'.format(name, href)
            one = '\n{}\n{}\n\n'.format(name, href)
            one = '\n{}\n\n[{}]({})\n\n'.format(name,href,href)
            links += one
    text = '### 【{}今日新闻】\n{}'.format(department, links)
    return text


def get_message():
    x, y, z = [], [], []
    try:
        x = one_process.get_today_or_week(department='人社', kw='，', mode='day')
    except:
        pass
    try:
        y = one_process.get_today_or_week(department='经信委', kw='，', mode='day')
    except:
        pass
    try:
        z = one_process.get_today_or_week(department='科委', kw='，', mode='day')
    except:
        pass
    textx = get_text('人社', x)
    texty = get_text('经信委', y)
    textz = get_text('科委', z)
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "今日政策文件如下",
            "text": "{}{}{}".format(textx, texty, textz)
        },
        "at": {
            "isAtAll": True
        }
    }
    return data


def save_message(msg):
    now = time.strftime('%Y-%m-%d-%H', time.localtime(time.time()))
    js = json.dumps(msg)
    fp = './msg_output/{}.json'.format(now)
    with open(fp, 'w', encoding='utf8') as x:
        x.write(js)
    return fp
def test_message():
    message = get_message()
    ddddd.send_message(message)
if __name__ == "__main__":
    # test_message()
    while True:

        time.sleep(1)
        time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新
        print(time_now)
        if time_now == "23:50:00":  # 此处设置每天定时的时间
            # 此处3行替换为需要执行的动作
            print("hello")
            message = get_message()
            fp = save_message(msg=message)
            print('{}保存成功'.format(time_now))
            time.sleep(5)
        if time_now == "09:00:00":
            #fp = './msg_output/{}.json'.format(ddddd.getYesterday())
            print(fp)
            # fp = './msg_output/{}.json'.format('2020-12-28-15')
            print('hello')
            with open(fp, 'r') as f:
                content = f.read()
                js = json.loads(content)
            print(js)
            ddddd.send_message(js)
            print('{}发送成功'.format(time_now))
            time.sleep(5)

    # time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新
    # message = get_message()
    # fp = save_message(msg=message)
    # print('{}保存成功'.format(time_now))
    #
    # with open(fpo, 'r') as f:
    #     content = f.read()
    #     js = json.loads(content)
    # print(js)

    # ddddd.send_message(message)
    # print(y)
    # print(z)
