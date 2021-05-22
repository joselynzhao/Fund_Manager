#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/5/20 下午4:34
# @Author  : Joselynzhao
# @Email   : zhaojing17@forxmail.com
# @File    : try1.py
# @Software: PyCharm
# @Desc    :

import requests
import time
import execjs

#构造一个接口
def getUrl(fscode):
    head = 'http://fund.eastmoney.com/'
    tail = '.html'
    return head+fscode+tail


# 根据基金代码获取净值
def getWorth(fscode):
    content = requests.get(getUrl(fscode))
    jsContent = execjs.compile(content.text)

    name = jsContent.eval('fS_name')
    code = jsContent.eval('fS_code')
    # 单位净值走势
    netWorthTrend = jsContent.eval('Data_netWorthTrend')
    # 累计净值走势
    ACWorthTrend = jsContent.eval('Data_ACWorthTrend')

    netWorth = []
    ACWorth = []

    for dayWorth in netWorthTrend[::-1]:
        netWorth.append(dayWorth['y'])

    for dayACWorth in ACWorthTrend[::-1]:
        ACWorth.append(dayACWorth[1])
    print(name, code)
    return netWorth, ACWorth


def getAllCode():
    url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    content = requests.get(url)
    jsContent = execjs.compile(content.text)
    rawData = jsContent.eval('r')
    allCode = []
    for code in rawData:
        allCode.append(code[0])
    return allCode


allCode = getAllCode()

netWorthFile = open('./netWorth.csv', 'w')
ACWorthFile = open('./ACWorth.csv', 'w')

for code in allCode:
    try:
        netWorth, ACWorth = getWorth(code)
    except:
        continue
    if len(netWorth) <= 0 or len(ACWorth) < 0:
        print(code + "'s' data is empty.")
        continue
    netWorthFile.write("\'" + code + "\',")
    netWorthFile.write(",".join(list(map(str, netWorth))))
    netWorthFile.write("\n")

    ACWorthFile.write("\'" + code + "\',")
    ACWorthFile.write(",".join(list(map(str, ACWorth))))
    ACWorthFile.write("\n")
    print("write " + code + "'s data success.")

netWorthFile.close()
ACWorthFile.close()
