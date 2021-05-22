#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/5/20 下午8:24
# @Author  : Joselynzhao
# @Email   : zhaojing17@forxmail.com
# @File    : priceRate.py
# @Software: PyCharm
# @Desc    :


import requests
import random
import time
import pandas as pd
import execjs
import json
from tqdm import tqdm
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

def getPriceRate():
    headers = {'User-Agent': random.choice(user_agent_list), 'Referer': referer_list[0]}
    content = requests.get('http://fund.ijijin.cn/data/Net/gz/all_priceRate_desc_0_0_1_9999_0_0_0_jsonp_g.html',headers=headers).text
    # print(content['data'])
    # print(content)
    content_=content[2:-1]
    dataanderror = json.loads(content_)
    data = dataanderror['data']
    print(len(data))
    df = pd.DataFrame(data)  # 转化为ｄｆ＝格式
    df = df.transpose()
    df = df[['code','date','name','preprice','price','priceRate','net','rate']]
    df[['preprice','price','priceRate','net','rate']]=df[['preprice','price','priceRate','net','rate']].apply(pd.to_numeric)
    df.columns=['编码','日期','名称','基金净值','当日估值','估值增长','单位净值','日增长率']
    # print(df)
    # return data
    try:
        t= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(t)
        df.to_excel(f'估值all_{t}.xlsx', 'all', index=None, encoding='utf-8')
    except Exception as e:
        print(e)

def getUrl(fscode):
    return  'http://fund.10jqka.com.cn/data/client/myfund/'+fscode

def getAllInfo():
    headers = {'User-Agent': random.choice(user_agent_list), 'Referer': referer_list[0]}
    content = requests.get('http://fund.ijijin.cn/data/Net/gz/all_priceRate_desc_0_0_1_9999_0_0_0_jsonp_g.html',
                           headers=headers).text
    # print(content['data'])
    # print(content)
    content_ = content[2:-1]
    dataanderror = json.loads(content_)
    data_raw = dataanderror['data']
    data = list(data_raw.values())
    df = pd.DataFrame(data)[:-1]  # 转化为ｄｆ＝格式
    # df = pd.DataFrame(data)  # 转化为ｄｆ＝格式
    df = df[['code','date','preprice','price','priceRate','rate']]
    df[['code']] = df[['code']].astype(str)
    # columns1 = df.columns.tolist()
    length = len(df)
    # df = df.transpose()
    #添加更多的信息
    data_add = []
    for i in tqdm(range(length)):
    # for i in range(length):
        one = data[i]
        code = one['code']
        # print(f"正在爬取编码{code}的基金信息……")
        headers2 = {'User-Agent': random.choice(user_agent_list), 'Referer': referer_list[0]}
        content2 = requests.get(getUrl(str(code)), headers=headers2).text
        try:
            content_2 = json.loads(content2)
            data2 = content_2['data'][0]
        except Exception as e:
            print(e)
            data2=[]
        data_add.append(data2)
    df2 = pd.DataFrame(data_add)
    df2 = df2[['code','name', 'fundtype', 'asset', 'clrq', 'levelOfRisk', 'manager', 'maxStar', 'net', 'orgname', 'sgstat',
         'shstat', 'week', 'month', 'tmonth', 'hyear', 'year', 'tyear']]  # 取出我要用的数据
    df2[['code']] = df2[['code']].astype(str)
    # columns2=df2.columns.tolist()
    # columns_join = [one for one in columns1 if  one in columns2]
    # print(columns_join)
    # df2 = df2.transpose()
    # df3 = pd.concat([df,df2],axis=1,join_axes=[df['code']])
    # df3 = pd.concat(df,df2) #气死了，结果还是不对
    df3 = pd.concat([df,df2],axis=1,join='outer') #气死了，结果还是不对
    # df3 = pd.concat([df3[:3],df3[3:]],axis=1,join='outer') #气死了，结果还是不对
    # df3 = pd.merge(df,df2) #气死了，结果还是不对
    # df3 = pd.merge(df,df2, how='outer',on={'code'}) #气死了，结果还是不对
    print(df3)
    df3 = df3[['code','name', 'fundtype', 'asset', 'clrq', 'levelOfRisk', 'manager', 'maxStar',  'orgname', 'sgstat',
         'shstat','date','preprice','price','priceRate','net','rate', 'week', 'month', 'tmonth', 'hyear', 'year', 'tyear']]
    # print(df3.columns.to_list())
    df3.columns=['编码１','编码２','名称', '类型', '规模(亿)', '成立时间', '风险等级', '基金经理', '基金评级',  '基金公司', '申购状态',
         '赎回状态','当前日期','基金净值','当日估值','估值增长(%)','当日单位净值','日增长率-收盘(%)', '近1周涨幅(%)', '近1月涨幅(%)', '近3月涨幅(%)', '近6月涨幅(%)', '近1年涨幅(%)', '近3年涨幅(%)']
    #转换数据类型
    # df3[['成立时间','当前日期']] = df3[['成立时间','当前日期']].apply(pd.to_datetime)
    df3[['规模(亿)','基金净值','当日估值','估值增长(%)','当日单位净值','日增长率-收盘(%)', '近1周涨幅(%)', '近1月涨幅(%)', '近3月涨幅(%)', '近6月涨幅(%)', '近1年涨幅(%)', '近3年涨幅(%)']].apply(pd.to_numeric)
    # df3 = df3.rename(columns={'name':'名称', 'fundtype':'类型', 'asset':'规模(亿)', 'clrq':'成立时间', 'levelOfRisk':'风险等级', 'manager':'基金经理', 'maxStar':'基金评级',  'orgname':'基金公司', 'sgstat':'申购状态',
    #      'shstat':'赎回状态','date':'当前日期','preprice':'基金净值','price':'当日估值','priceRate':'估值增长','net':'当日单位净值','rate':'日增长率', 'week':'近1周涨幅', 'month':'近1月涨幅', 'tmonth':'近3月涨幅', 'hyear':'近6月涨幅', 'year':'近1年涨幅', 'tyear':'近3年涨幅'},inplace=True)
    # df3 = df3.transpose()
    # result = df3[['code', 'date', 'name', 'preprice', 'price', 'priceRate', 'net', 'rate']]
    # print(result)

    try:
        t= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(t)
        df3.to_excel(f'基金汇总_{t}.xlsx', 'all', index=None, encoding='utf-8')
    except Exception as e:
        print(e)









if __name__=='__main__':
    # print(getUrl(519918))
    # getWorth(519918)
    getPriceRate()