#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/5/20 下午5:14
# @Author  : Joselynzhao
# @Email   : zhaojing17@forxmail.com
# @File    : try2.py
# @Software: PyCharm
# @Desc    :

#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random
import time
from requests import get


# user_agent列表
user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
]

# referer列表
referer_list = [
    'http://fund.eastmoney.com/110022.html',
    'http://fund.eastmoney.com/110023.html',
    'http://fund.eastmoney.com/',
    'http://fund.eastmoney.com/110025.html'
]


def get_html(baseUrl):
    # 获取一个随机user_agent和Referer
    headers = {'User-Agent': random.choice(user_agent_list), 'Referer': random.choice(referer_list)}
    try:
        resp = get(baseUrl, headers=headers)
        # print(resp.status_code)
        if resp.status_code == 200:
            # print(resp.content)
            return resp.text
        print("没有爬取到相应的内容")
        return None
    except RequestException:
        print("没有爬取到相应的内容")
        return None


if __name__ == "__main__":

    t = time.time()
    rt = int(round(t * 1000))

    baseUrl = "http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery183006797018539211241_1593855325551&fundCode=004070&pageIndex=1&pageSize=20&startDate=2020-06-01&endDate=2020-07-01&_=" + str(rt)
    print(baseUrl)
    data = get_html(baseUrl)
    print(data)