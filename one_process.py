import datetime

import requests
import time
import urllib3

# from multiprocessing.dummy import Pool
# import pandas as pd

urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}

urls = {
    '人社': 'http://rlsbj.cq.gov.cn/igs/front/search.jhtml?code=4b5c979955214c8795de1934f5b5a405&timeOrder=desc&siteId=75&ordryBy=time&position=&pageSize=15',
    '经信委': 'https://jjxxw.cq.gov.cn/igs/front/search.jhtml?code=6f2ae04649c34fa1bdcf611f2e4b5376&timeOrder=desc&siteId=39&ordryBy=time&position=&pageSize=15',
    '科委': 'http://kjj.cq.gov.cn/igs/front/search.jhtml?code=06ea63ecd64542c7b1ce37f54906a4df&timeOrder=desc&siteId=49&ordryBy=time&position=&pageSize=15'
}


def get_today_or_week(department='人社', kw='补贴', mode='day'):
    """
    :param department: 部门=>['人社','经信委','科委']
    :param kw: 搜索关键字
    :param mode: 模式，day或者week
    :return: 结果的字典列表,没有则是空列表
    """
    params = {
        'searchWord': kw,
        'pageNumber': 1,
        'advancedQuery.timeRange': mode
    }
    try:
        response = requests.get(url=urls[department], params=params, headers=headers, verify=False)
        print(response.json())
        total = int(response.json()['page']['total'])
        totalPages = int(response.json()['page']['totalPages'])
    except:
        total = 0
        totalPages = 0
    result = []
    if total != 0:
        for pg in range(1, totalPages + 1):
            print('{},第-{}-页'.format(kw, pg))
            params = {
                'searchWord': kw,
                'pageNumber': pg,
                'advancedQuery.timeRange': mode
            }
            try:
                response = requests.get(url=urls[department], params=params, headers=headers, verify=False)
                time.sleep(5)
                # print(response.json())
                content = response.json()['page']['content']
                result += content
            except:
                pass
    print(result)
    return DelRepeat(result, 'url')


def get_all_info_by_day_or_week(department=None, mode='day', kw=None):
    """
    :param department:
    :param mode:
    :param kw:
    :return: 字典列表
    """
    departments = department
    if departments is None:
        departments = ['人社', '经信委', '科委']
    # departments = ['人社']
    keywords = kw
    if keywords is None:
        keywords = ['补贴', '申报', '新职业', '就业提升', '职业技能']
    # keywords = ['补贴', '申报']

    print(keywords, departments)
    results = []
    for department in departments:
        print('正在爬:', department)
        print('*' * 30)
        for keyword in keywords:
            # time.sleep(3)
            result = get_today_or_week(department=department, kw=keyword, mode='week')
            results += result
    if mode == 'day' and results:
        results = list(filter(lambda x: x['PUBDATE'][:10] in [datetime.date.today() + datetime.timedelta(-1),
                                                              time.strftime("%Y-%m-%d", time.localtime())], results))
    return DelRepeat(results, 'url')


# datetime.date.today() + datetime.timedelta(-1)
# 列表中嵌套字典按照指定键去重
def DelRepeat(data, key):
    new_data = []  # 用于存储去重后的list
    values = []  # 用于存储当前已有的值
    for d in data:
        if d[key] not in values:
            new_data.append(d)
            values.append(d[key])
    return new_data


def to_mysql():
    pass


if __name__ == '__main__':
    # pass
    # results = get_all_info_by_day_or_week(mode='week')
    # df = pd.DataFrame().from_dict(results)
    # df.to_csv('test.csv',encoding="utf_8_sig")
    # print(results)
    # df = pd.DataFrame().from_dict(results)
    # print(df[['title', 'trs_time', 'trs_site', 'url']].values.tolist())
    # df[['title', 'trs_time', 'trs_site', 'url']].to_csv('all_test.csv',encoding='utf_8_sig')
    get_today_or_week()
    print('ssss')
