#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/5/23 下午3:22
# @Author  : Joselynzhao
# @Email   : zhaojing17@forxmail.com
# @File    : Score_Computer.py
# @Software: PyCharm
# @Desc    :

import  math


def sizeScore(one):
    if one == '--': return 1
    one = float(one)
    if one < 100 and one >= 30:
        return 6 - abs(one - 60) / 10
    elif (one >= 100 and one < 300) or (one < 30 and one >= 10):
        return 1
    else:
        return 0


def startHBLScore(one):
    if one == '--': return 1
    one = float(one)
    if one >= 500:
        return 6
    elif one >= 300:
        return 4
    elif one >= 100:
        return 2
    else:
        return 1


def Normolization(number_list):
    # new_number = []
    for i,e in enumerate(number_list):
        number_list[i] =(float(e-min(number_list))/(max(number_list)-min(number_list)))
    return number_list


def yearHBLScore(one):
    if one == '--': return 1
    one = float(one)
    if one >= 30 and one <40:
        return 4
    if one >=20 and one <30:
        return 3
    if one >=10 and one <20:
        return 2
    if one < 10 or one >40:
        return 1



def workdaysScore(one):
    if one == '--': return 1
    one = float(one)
    if one >= 3000:
        return 5
    elif one >= 2000:
        return 4
    elif one >= 1000:
        return 3
    else:
        return 1


def JLlevelScore(one):
    if one == '--': return 1
    one = float(one)
    return one / 2


def JJlevelScore(one):
    if one == '--': return 1
    one = float(one)
    if math.isnan(one):  # 是空则返回０
        return 1
    else:
        return one


def tyearZFScore(one):
    if one == '--': return 1
    one = float(one)
    if one >= 150:
        return 6
    elif one >= 125:
        return 5
    elif one >= 100:
        return 4
    elif one >= 75:
        return 3
    elif one >= 50:
        return 2
    else:
        return 1


def HCScore(one):
    if one == '--': return 1
    one = float(one)
    if one <= 10:
        return 5
    elif one <= 15:
        return 4
    elif one <= 20:
        return 3
    elif one <= 25:
        return 2
    else:
        return 1


def HC_justScore(zf, hc):
    return zf / hc / 2


def XPScore(one):
    if one == '--': return 1
    one = float(one)
    if one >= 3:
        return 6
    elif one >= 2.5:
        return 5
    elif one >= 2:
        return 4
    elif one >= 1.5:
        return 3
    elif one >= 1:
        return 2
    else:
        return 1


def BDScore(one):
    if one == '--': return 1
    one = float(one)
    if one <= 20:
        return 4
    elif one <= 25:
        return 3
    elif one <= 30:
        return 2
    else:
        return 1

def LJJZScore(one):
    if one == '--': return 1
    one = float(one)
    return one/1.5
def DWJZ_LJJZScore(dw, lj):
    if lj < 4.0: return 0
    return lj - dw


def FRScore(one):
    if one == '--':
        return 1
    one = float(one)
    if math.isnan(one): return 1
    return (int(one / 10) + 1) / 2.0

'''
下面通过硬性指标筛选好基金
'''

def isGood(one,arrow,stand):# 针对数字类型
    if one == '--': return 0
    one = float(one)
    if math.isnan(one):return 0
    if arrow==0: #xiao genghao
        if one <=stand:return 1
        else:return 0
    elif arrow == 1:# da genghao
        if one >=stand:return 1
        else:return 0


def isGoodStartTime(one,standerd=2018):
    if int(one.strip('-')[0])<=standerd:
        return 1
    else:return 0






