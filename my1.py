#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/5/20 下午4:58
# @Author  : Joselynzhao
# @Email   : zhaojing17@forxmail.com
# @File    : my1.py
# @Software: PyCharm
# @Desc    :

import requests
import random
import time
import pandas as pd
import execjs
import json
# referer列表
referer_list = [
    'http://fund.10jqka.com.cn/'
    'http://fund.eastmoney.com/110022.html',
    'http://fund.eastmoney.com/110023.html',
    'http://fund.eastmoney.com/',
    'http://fund.eastmoney.com/110025.html'
]
# user_agent列表
user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
]

fund_list=['100020',
    '002959',
    '470058',
    '001857',
    '240011',
    '180012',
    '260101',
    '570008',
    '090018',
    '100060',
    '001500',
    '005918',
    '001716',
    '570001',
    '004997',
    '519068',
    '519736',
    '003095',
    '001938',
    '166001',
    '161725',
    '162605',
    '005827',
    '260108',
    '163406'
]

def getUrl(fscode):
    return  'http://fund.10jqka.com.cn/data/client/myfund/'+fscode

def getWorth(fscode):
    headers = {'User-Agent': random.choice(user_agent_list), 'Referer': referer_list[0]}
    content = requests.get(getUrl(fscode),headers=headers).text
    # print(content['data'])
    content_ = json.loads(content)
    data = content_['data'][0]
    return data

def updata():
    #init

    datas = []
    for code in fund_list:
        data = getWorth(code)
        datas.append(data)
    # print(datas)
    df = pd.DataFrame(datas) #转化为ｄｆ＝格式
    df = df[['code','name','fundtype','asset','clrq','levelOfRisk','manager','maxStar','net','orgname','sgstat','shstat','week','month','tmonth','hyear','year','tyear']] #取出我要用的数据
    df.columns = ['编码','名称','类型','规模(亿)','成立时间','风险等级','经理','评级','单位净值','基金公司','申购状态','赎回状态','周涨幅','月涨幅','３月涨幅','６月涨幅','年涨幅','３年涨幅'] #重名列名
    df[['规模(亿)','评级','单位净值','周涨幅','月涨幅','３月涨幅','６月涨幅','年涨幅','３年涨幅']]=df[['规模(亿)','评级','单位净值','周涨幅','月涨幅','３月涨幅','６月涨幅','年涨幅','３年涨幅']].apply(pd.to_numeric)
    try:
        t= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(t)
        df.to_excel(f'基金_{t}.xlsx', '关注', index=None, encoding='utf-8')
    except Exception as e:
        print(e)
    # print(df)






if __name__=='__main__':
    # print(getUrl(519918))
    # getWorth(519918)
    updata()
