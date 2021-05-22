#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/5/20 下午2:24
# @Author  : Joselynzhao
# @Email   : zhaojing17@forxmail.com
# @File    : main.py
# @Software: PyCharm
# @Desc    : 


import requests
import time
import pandas as pd
# import openpyxl

# 包含全部基金信息的网址：　http://fund.eastmoney.com/fund.html#os_0;isall_0;ft_;pt_1

if __name__ == '__main__':
    for j in range(1, 2):
        # url=f'http://fund.10jqka.com.cn/datacenter/jz/'
        # url =f'http://fund.eastmoney.com/fund.html#os_0;isall_0;ft_;pt_1,desc&page={j},200&dt=1597126258333&atfc=&onlySale=0'
        # url = f'http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=1&letter=&gsid=&text=&sort=zdf,desc&page={j},200&dt=1597126258333&atfc=&onlySale=0'
        # 基金经理信息
        url =f'http://fund.eastmoney.com/Data/FundDataPortfolio_Interface.aspx?dt=14&mc=returnjson&ft=all&pn=5000&pi=1&sc=abbname&st=asc'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER'
        }
        resp = requests.get(url, headers=headers).text
        str_ = resp[102:]
        # list1 = eval(str_.split(",count")[0])
        list1 = eval(str_.split(",record")[0])
        print(f'正在爬取第{j}页')
        print(f'本页爬取{len(list1)}条数据')

        num = []
        name = []
        today_price = []
        yesterday_price = []
        day_value = []
        day_value_rate = []
        subscription_status = []
        redemption_status = []
        service_charge = []

        for i in range(len(list1)):
            # 1、基金代码号
            num.append(list1[i][0])
            # 2、股票名称
            name.append(list1[i][1])
            # 3、今日基金净额
            today_price.append(list1[i][3])
            # 4、昨日基金净额
            yesterday_price.append(list1[i][5])
            # 5、日增长值
            day_value.append(list1[i][7])
            # 6、日增长率
            day_value_rate.append(list1[i][8])
            # 7、申购状态
            subscription_status.append(list1[i][9])
            # 8、赎回状态
            redemption_status.append(list1[i][10])
            # 9、手续费
            service_charge.append(list1[i][17])

        df = pd.DataFrame()
        df['基金代码'] = num
        df['基金名称'] = name
        df['今日单位净值'] = today_price
        df['昨日单位净值'] = yesterday_price
        df['日增长值'] = day_value
        df['日增长率\n%'] = day_value_rate
        df['申购状态'] = subscription_status
        df['赎回状态'] = redemption_status
        df['手续费'] = service_charge

        try:
            df.to_excel(f'基金{j}.xlsx', '基金信息', index=None, encoding='utf-8')


        except Exception as e:
            print(e)

    time.sleep(1)