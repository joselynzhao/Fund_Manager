#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/5/25 下午3:38
# @Author  : Joselynzhao
# @Email   : zhaojing17@forxmail.com
# @File    : Fund_Manager_v3.py
# @Software: PyCharm
# @Desc    :　修改了读取文件的格式。


import requests
import random
import time
import pandas as pd
import execjs
import json
from tqdm import tqdm
import math
import numpy as np
from Score_Computer import *
from Codes_infor import *
import datetime

# http://fund.eastmoney.com/005296.html
# url1 = 'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&secids=1.000001,0.399001&invt=2&fields=f2,f3,f4,f6,f12,f104,f105,f106&ut=267f9ad526dbe6b0262ab19316f5a25b&cb=jQuery18307458225946461923_1621588092653&_=1621588092705'
'''
0 上证指数　ｆ104涨　
'''


class Fund_manager():
    def __init__(self):
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        date = t.split(' ')[0]
        self.date = date
        # self.care_list = care_list
        self.headers = {'User-Agent': random.choice(user_agent_list), 'Referer': referer_list[0]}  # 每次运行的时候都会重新生成头部

    def Runscore(self, input_file_name):  # 制定跑哪几列分数
        codes_infor = pd.read_excel(f'{input_file_name}.xlsx', dtype=str)  # 全部读取为字符串格式

        query_codes = codes_infor['code']
        query_type = codes_infor['type']
        # dataInfors = codes_infor #用codeInfor来初始化
        get_Infors = pd.DataFrame()
        for i in tqdm(range(len(query_codes))):
            code = query_codes[i]
            FR = pd.Series(self.getFourRank(code))
            TTJJ = pd.Series(self.getWorth_infor1(code))  # 返回很多信息
            THS = pd.Series(self.getInfo_fromApp(code))
            Water = pd.Series(self.getWaterLevel(code))
            # RDZF = pd.Series(self.getRZDF(code))
            # 　处理获得的数据
            # FR 和同花顺也不需要处理　全选
            TTJJ = TTJJ[['code', 'name', 'asset', 'clrq', 'levelOfRisk', 'manager', 'maxStar', 'totalnet1',
                         'orgname', 'week', 'month', 'tmonth', 'hyear', 'year', 'tyear']]
            code_infor = pd.DataFrame()
            code_infor = pd.concat([code_infor, FR, TTJJ, THS, Water], axis=0)
            # code_infor.loc['Source'] = col_code_name
            code_infor.columns = [code]
            # get_Infors = get_Infors.append(code_infor,ignore_index=True)
            get_Infors = pd.concat([get_Infors, code_infor], axis=1)
        # 一次行抓取最后一部分数据
        get_Infors = get_Infors.transpose()
        codes_infor.set_index(['code'], inplace=True)
        value_infor = pd.DataFrame(self.getWorth_Valuation_forList(query_codes))
        value_infor = value_infor[['priceRate']]
        get_Infors = pd.concat([codes_infor, get_Infors, value_infor], axis=1, join='outer')

        # 总共取这些数据
        get_Infors = get_Infors[[
            'code', 'type', 'name', 'JJType', 'maxStar', 'clrq', 'levelOfRisk', 'manager', 'JLlevel', 'orgname',
            'GPstock',
            'FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year', 'FR_nowyear', 'FR_hyear', 'FR_tmonth', 'FR_month',
            'FR_week',
            'asset', 'totalnet1', 'DWJZ', 'HC', 'XP', 'BD', 'priceRate',
            'week', 'month', 'tmonth', 'hyear', 'year', 'tyear', 'fyear', 'startZF',
            'manageHBL', 'yearHBL',
            'manageDay', 'workDay',
            'Hwater', 'water',
        ]]

        print(get_Infors.columns.tolist())
        # 将部分数据转为浮点类型
        get_Infors[[
            'FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year', 'FR_nowyear', 'FR_hyear', 'FR_tmonth', 'FR_month',
            'FR_week',
            'asset', 'totalnet1', 'DWJZ', 'HC', 'XP', 'BD', 'priceRate',
            'week', 'month', 'tmonth', 'hyear', 'year', 'tyear', 'fyear', 'startZF',
            'manageHBL', 'yearHBL',
            'manageDay', 'workDay',
            'Hwater', 'water']] = get_Infors[[
            'FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year', 'FR_nowyear', 'FR_hyear', 'FR_tmonth', 'FR_month',
            'FR_week',
            'asset', 'totalnet1', 'DWJZ', 'HC', 'XP', 'BD', 'priceRate',
            'week', 'month', 'tmonth', 'hyear', 'year', 'tyear', 'fyear', 'startZF',
            'manageHBL', 'yearHBL',
            'manageDay', 'workDay',
            'Hwater', 'water']].apply(pd.to_numeric, errors='ignore')

        # 获取数据评分处理
        # comp_in = get_Infors[
        #     ['FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year', 'FR_nowyear', 'FR_hyear', 'FR_tmonth', 'FR_month',
        #      'FR_week',
        #      'asset', 'totalnet1', 'DWJZ', 'HC', 'XP', 'BD','priceRate',
        #      'week', 'month', 'tmonth', 'hyear', 'year', 'tyear', 'fyear', 'startZF',
        #      'manageHBL', 'yearHBL', 'manageDay', 'workDay']]
        # raw_data = pd.read_excel(f'Infors/信息汇总_{self.date}_{input_file_name}.xlsx')
        comp_out = self.getFundScore(get_Infors)  # h获得总分
        comp_out.set_index(get_Infors['code'], inplace=True)
        get_Infors = pd.concat([get_Infors, comp_out], axis=1)
        try:
            get_Infors.to_excel(f'Infors/信息汇总_{self.date}_{input_file_name}.xlsx', '信息', index=None, encoding='utf-8')
        except Exception as e:
            print(e)

        OPs = self.getOP(get_Infors)
        OPs.set_index(get_Infors['code'], inplace=True)
        get_Infors = pd.concat([get_Infors, OPs], axis=1)
        # col = ['code', 'type', 'name', 'JJType', 'maxStar', 'clrq', 'levelOfRisk', 'manager', 'JLlevel', 'orgname',
        #        'GPstock',
        #        'FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year', 'FR_nowyear', 'FR_hyear', 'FR_tmonth', 'FR_month',
        #        'FR_week',
        #        'asset', 'totalnet1', 'DWJZ', 'HC', 'XP', 'BD', 'priceRate', 'week', 'month', 'tmonth', 'hyear', 'year',
        #        'tyear', 'fyear', 'startZF', 'manageHBL', 'yearHBL', 'manageDay', 'workDay', 'Hwater', 'water']

        SCORE = get_Infors[[
            'code', 'type', 'OPs', 'Score','Hwater', 'water', 'priceRate','year', 'name', 'JJType', 'maxStar', 'GPstock', 'manager',
            'HC', 'XP', 'BD',
            'week', 'month', 'tmonth', 'hyear', 'year', 'tyear', 'fyear',
        ]]
        # 　主要是根据根数来看操作
        # OP_In = get_Infors[['JJType', ]]
        # OP = self.getOP()
        SCORE.sort_values(by='Score', inplace=True, ascending=False)  # sort
        try:
            SCORE.to_excel(f'Scores/汇总_{self.date}_{input_file_name}.xlsx', '信息', index=None, encoding='utf-8')
        except Exception as e:
            print(e)

        # 试着进行操作指示

    def getOP(self, df):
        Comp = pd.DataFrame()

        def isStable(hc, bd):
            if hc < 10 and bd < 15:
                return 1
            else:
                return 0

        def isExc(hc, bd):
            if hc > 20 and bd > 25:
                return 1
            else:
                return 0

        def isUprise(week, month):
            if week > 1 and month > 4:
                return 1
            else:
                return 0

        def isDown(week):
            if week < -1:
                return 1
            else:
                return 0

        # Comp['isStable'] = pd.Series(map(isStable, df['HC'],df['BD']))
        # Comp['isExc'] = pd.Series(map(isExc,df['HC'],df['BD']))
        # Comp['isUprise'] = pd.Series(map(isUprise,df['week'],df['month']))
        # Comp['isDown']  = pd.Series(map(isDown,df['week']))
        def OPs_maker(hc, bd, week, month,tmonth, preprize, hwater, year):
            # if hc < 10 and bd < 15 and week > 0 and month > 0 and year > 0:
            #     return "稳定上升，持续定投"
            # elif hc < 10 and bd < 15 and week < 0 and month < 0:
            #     return "稳定下跌，建议抛售"
            # elif hc > 20 and bd > 25 and hwater < 85 and week > 0 and month > 0 and preprize < -1:
            #     return "激进上升，今日买入"
            # elif hc > 20 and bd > 25 and hwater > 85 and week > 0 and month > 0 and preprize < -1:
            #     return "激进上升，高估值，慎买"
            # elif hc > 20 and bd > 25 and hwater > 85 and week > 0 and month > 0 and preprize > 1:
            #     return "激进上升，高估值，今日卖出"
            # elif hc > 20 and bd > 25 and hwater > 85 and week < 0 and month > 0 and preprize > 0:
            #     return "激进回撤，今日卖出"
            # elif hc > 20 and bd > 25 and hwater < 85 and week < 0 and preprize < -1:
            #     return "激进下跌，今日买入"
            # elif hc > 20 and bd > 25 and hwater < 85 and week > 0 and month > 0 and preprize <1 and preprize >-1:
            #     return "激进上升，低估值，今日稳定"
            # elif hc > 20 and bd > 25 and hwater > 85 and week > 0 and month > 0 and preprize <1 and preprize >-1:
            #     return "激进上升，高估值，今日稳定"
            # # elif hc > 20 and bd > 25 and hwater < 85 and week < 0 : return "激进下跌，待降买入"
            # elif hc >= 10 and hc <= 20 and week > 0 and month > 0 and hwater < 85:
            #     return "中等上升，低估值，可定投"
            # elif hc >= 10 and hc <= 20 and week > 0 and month > 0 and hwater > 85:
            #     return "中等上升，高估值，少量定投"
            # elif hc >= 10 and hc <= 20 and week < 0 and month > 0 and hwater > 85:
            #     return "中等回撤，卖出或买入"
            # elif hc >= 10 and hc <= 20 and week < 0 and month < 0 and hwater < 85:
            #     return "中等下跌，卖出或买入"
            # else:
            #     pass

            #version 2
            # if hc+bd<20:
            #     if week>0 and month>0 and year>3 :return "稳定上升，可定投"
            #     if week<0 and month <0 :return "稳定下跌，可抛售"
            # else:
            #     if hc <20:#低风险
            #         if bd < 25 : #不用关注日涨幅
            #             if week >0 and month>0 : #持续上升阶段
            #                 if hwater<0.8 : return "低小上升，低估值，可定投"
            #                 else: return "低小上升，高估值，少定投或卖出"
            #             if week >0 and month <0: #回升阶段
            #                 if hwater<0.8 : return "低小回升，低估值，可定投"
            #                 else: return "低小回升，高估值，少定投"
            #             if week <0 and month>0 : #回撤阶段
            #                 if hwater<0.8 : return "低小回撤，低估值，可定投"
            #                 else: return "低小回撤，高估值，少定投或卖出"
            #             if week <0 and month<0: # 持续下降阶段
            #                 if hwater<0.8 : return "低小下跌，低估值，慎定投"
            #                 else: return "低小下跌，高估值（不会发生）"
            #         else: #bd >=25 关注日涨幅
            #             if month >0 and tmonth>0 : #持续上升阶段
            #                 if hwater<0.8:
            #                     if preprize >1: return "低大上升，低估值"
            #                     elif preprize <1 and preprize>-1: return "低大上升，低估值"
            #                     else:return "低大上升，低估值，今日可买"
            #                 else:
            #                     if preprize >1:return "低大上升，高估值，今日可卖"
            #                     elif preprize <1 and preprize>-1:return "低大上升，高估值"
            #                     else:"低大上升，高估值，今日慎买"
            #             if month >0 and tmonth <0: #回升阶段
            #                 if hwater<0.8:
            #                     if preprize >1:return "低大回升，低估值"
            #                     elif preprize <1 and preprize>-1:return "低大回升，低估值"
            #                     else:return "低大回升，低估值，今日可买"
            #                 else:return "低大回升，高估值(不发生)"
            #                     # if preprize >1:return "低大回升，高估值，今日可卖"
            #                     # elif preprize <1 and preprize>-1:return "低大回升，高估值，今日稳定"
            #                     # else:return "低大回升，高估值，今日慎买"
            #             if month <0 and tmonth>0 : #回撤阶段
            #                 if hwater<0.8:
            #                     if preprize >1:return "低大回撤，低估值，今日可卖"
            #                     elif preprize <1 and preprize>-1:return "低大回撤，低估值"
            #                     else:return "低大回撤，低估值，今日可买"
            #                 else:
            #                     if preprize >1:return "低大回撤，高估值，今日可卖"
            #                     elif preprize <1 and preprize>-1:return "低大回撤，高估值"
            #                     else:return "低大回撤，高估值，今日慎买"
            #             if month <0 and tmonth<0: # 持续下降阶段
            #                 if hwater<0.8:
            #                     if preprize >1:return "低大下跌，低估值，今日可卖"
            #                     elif preprize <1 and preprize>-1:return "低大下跌，低估值"
            #                     else:return "低大下跌，低估值，今日慎买"
            #                 else:
            #                     return "低大下跌，高估值（不会发生）"
            #                     # if preprize >1:
            #                     # elif preprize <1 and preprize>-1:
            #                     # else:
            #     else: # hc>20 高风险　不区分波动，因为波动不会小，关注日涨幅
            #         if month > 0 and tmonth > 0:  # 持续上升阶段　（卖）
            #             if hwater < 0.8:
            #                 if preprize > 1:return "高大上升，低估值"
            #                 elif preprize < 1 and preprize > -1:return "高大上升，低估值"
            #                 else:return "高大上升，低估值，今天可买"
            #             else:
            #                 if preprize > 1:return "高大上升，高估值，今日可卖"
            #                 elif preprize < 1 and preprize > -1:return "高大上升，高估值"
            #                 else:return "高大上升，高估值，今日慎买"
            #         if month > 0 and tmonth < 0:  # 回升阶段　（买）
            #             if hwater < 0.8:
            #                 if preprize > 1:return "高大回升，低估值"
            #                 elif preprize < 1 and preprize > -1:return "高大回升，低估值"
            #                 else:return "高大回升，低估值，今日可买"
            #             else:
            #                 return "高大回升，高估值（不发生）"
            #         if month < 0 and tmonth > 0:  # 回撤阶段
            #             if hwater < 0.8:
            #                 if preprize > 1:return "高大回撤，低估值"
            #                 elif preprize < 1 and preprize > -1:return "高大回撤，低估值"
            #                 else:return "高大回撤，低估值，今日慎买"
            #             else:
            #                 if preprize > 1:return "高大回撤，高估值，今日可卖"
            #                 elif preprize < 1 and preprize > -1:return "高大回撤，高估值"
            #                 else:return "高大回撤，高估值，今日慎买"
            #         if month < 0 and tmonth < 0:  # 持续下降阶段
            #             if hwater < 0.8:
            #                 if preprize > 1:return "高大下跌，低估值"
            #                 elif preprize < 1 and preprize > -1:return "高大下跌，低估值"
            #                 else:return "高大下跌，低估值，今日慎买"
            #             else:
            #                 return "高大下跌，高估值（不发生）"

            # version 3
            if hc+bd <20:
                if week > 0 and month > 0 and year > 3: return "稳定上升，一次性大量投放"
                if week < 0 and month < 0: return "稳定下跌，可抛售"
            else: #非债券类型
                if hc<20:
                    if bd<25:
                        return "低小，大量定投"
                    else: #bd>=25
                        if hwater<0.85:
                            if preprize<-1 or (week<1 and preprize<0.5):return "低大低，定投，今日大份买入"
                            else:return "低大低，定投"
                        else:#hwater>=85
                            if preprize<-1 or (week<1 and preprize<0.5):return "低大高，定投，今日小份买入"
                            elif preprize >1 or (week >1 and preprize>0.5):return "低大高，定投，今日可卖"
                            else :return "低大高，定投"
                else: #hc>=20
                    if hwater < 0.68:
                        if preprize < -1 or (week<1 and preprize<0):
                            return "高大低，定投，今日大份买入"
                        else:
                            return "高大低，定投"
                    elif hwater >= 0.68 and hwater < 0.85:
                        if month>0 and tmonth>0:
                            if preprize<-1 or (week<1 and preprize<0.5):return "高大中，上升，今日中份买入"
                            else: return "高大中，上升"
                        if month>0 and tmonth<0: #回升
                            if preprize<-1 or (week<1 and preprize<0.5):return "高大中，回升，今日中份买入"
                            else: return "高大中，回升"
                        if month<0 and tmonth>0:# 回撤
                            if preprize>1 or (week >1 and preprize>0.5):return "高大中，回撤，今日可卖"
                            else: return "高大中，回撤"
                        if month<0 and tmonth<0:#下跌
                            if preprize>1 or (week >1 and preprize>0.5):return "高大中，下跌，今日可卖"
                            else: return "高大中，下跌"
                    else:  # hwater>=0.85
                        if preprize<-1 or (week<1 and preprize<0.5) :return "高大高，今日小份买入"
                        if preprize>1 or (week >1 and preprize>0.5):return "高大高，今日可卖"
                        else: return "高大高"




        Comp['OPs'] = pd.Series(
            map(OPs_maker, df['HC'], df['BD'], df['week'], df['month'],df['tmonth'], df['priceRate'], df['Hwater'], df['year']))
        return Comp

        # print(0)

    def getRZDF(self, fscode):
        # 'http://gz-fund.10jqka.com.cn/?module=api&controller=index&action=chart&info=vm_fd_163406&start=0930&_=1621995244528'
        # 'http://gz-fund.10jqka.com.cn/?module=api&controller=index&action=chart&info=vm_fd_JSH108&start=0930&_=1621994890153'
        url = 'http://gz-fund.10jqka.com.cn/?module=api&controller=index&action=chart&info=vm_fd_' + fscode + '&start=0930'
        content = requests.get(url, headers=self.headers).text  # str类型
        try:
            _, baseline, raw_data = content.split('~')
        except Exception as e:
            print(e)
            return {'RZDF': -1000}
        try:
            baseline = float(baseline)
        except Exception as e:
            print(e)
            return {'RZDF': -1000}
        one_data = raw_data.split(';')[-1]
        time, end_data, _, _ = one_data.split(',')
        end_data = float(end_data)
        return {'RZDF': round((end_data - baseline) * 100 / (baseline), 2)}

    def getFourRank(self, fscode):  # 获得四分位排名
        url = 'http://fund.10jqka.com.cn/ifindRank/quarter_year_' + fscode + '.json'
        content = requests.get(url, headers=self.headers).text  # str类型
        try:
            jscontent = json.loads(content)
        except Exception as e:
            print(e)
        results = {}
        try:
            rawdata = jscontent['nowCommonTypeRank']
        except Exception as e:
            print(e)
            return results
        title = ['fyear', 'tyear', 'twoyear', 'year', 'nowyear', 'hyear', 'tmonth', 'month', 'week']
        for name in title:
            try:
                results['FR_' + name] = float(rawdata[name][2])
            except Exception as e:
                results['FR_' + name] = math.nan
        return results

    def getDWJZ(self, fscode):  # 单位净值数据
        url = 'http://fund.10jqka.com.cn/163406/json/jsondwjz.json'  # 单位净值数据、
        # url = 'http://fund.10jqka.com.cn/163406/json/jsonljjz.json'  # 累计净值数据、
        # url = 'http://fund.10jqka.com.cn/163406/json/jsonfqjz.json'  # 收益
        try:
            url = 'http://fund.10jqka.com.cn/ifindRank/quarter_year_' + fscode + '.json'
        except Exception as e:
            print(e)
            code = str(fscode)  # 转换为ｓｔｒ格式
            url = 'http://fund.10jqka.com.cn/ifindRank/quarter_year_' + code + '.json'

    def getWaterLevel(self, fscode):
        url = 'http://fund.10jqka.com.cn/' + fscode + '/json/jsonljjz.json'
        content = requests.get(url, headers=self.headers).text  # str类型
        try:
            raw_data = content.split('=')[1]
        except Exception as e:
            print(e)
            return {'Hwater': '000 ', 'water': '000'}
        raw_data = json.loads(raw_data)
        raw_data = pd.DataFrame(raw_data)
        try:
            raw_data.set_index([0], inplace=True)
        except Exception as e:
            print(e)
            return {'Hwater': '000 ', 'water': '000'}

        # if len(raw_data)>=400:
        #     raw_data = raw_data[len(raw_data)-400:]
        def getday(y, m, d, n):
            the_date = datetime.datetime(y, m, d)
            result_date = the_date + datetime.timedelta(days=n)
            d = result_date.strftime('%Y-%m-%d')
            d = ''.join(d.split('-'))
            return d

        year, month, day = self.date.split('-')

        dates = raw_data.index.tolist()
        today_subDay = 0
        today = year + month + day
        while (today not in dates):
            today_subDay -= 1
            today = getday(int(year), int(month), int(day), today_subDay)

        year_subDay = -366
        year_date = getday(int(year), int(month), int(day), year_subDay)
        if int(year_date) - int(dates[0]) > 6:
            while (year_date not in dates):
                year_subDay -= 1
                year_date = getday(int(year), int(month), int(day), year_subDay)
            index_year = dates.index(year_date)
            year_datas = raw_data[index_year:]
            year_max_value = float(max(year_datas[1]))
            year_base_value = float(year_datas.loc[year_date])
            today_value = float(year_datas.loc[today])
            if year_max_value != year_base_value:
                # hyear_max_index = hyear_datas.index(hyear_max_value)
                year_water = (today_value - year_base_value) / (year_max_value - year_base_value)

            else:
                year_min_value = float(min(year_datas[1]))
                year_water = (today_value - year_min_value) / (year_base_value - year_min_value)
            year_water = round(year_water, 4)
        else:
            year_water = -1000

        hyear_subDay = -183
        hyear_date = getday(int(year), int(month), int(day), hyear_subDay)
        if int(hyear_date) - int(dates[0]) > 6:
            while (hyear_date not in dates):
                hyear_subDay -= 1
                hyear_date = getday(int(year), int(month), int(day), hyear_subDay)
            index_hyear = dates.index(hyear_date)
            hyear_datas = raw_data[index_hyear:]
            hyear_max_value = float(max(hyear_datas[1]))
            hyear_base_value = float(hyear_datas.loc[hyear_date])
            today_value = float(hyear_datas.loc[today])
            if hyear_max_value != hyear_base_value:
                # hyear_max_index = hyear_datas.index(hyear_max_value)
                hyear_water = (today_value - hyear_base_value) / (hyear_max_value - hyear_base_value)
            else:
                hyear_min_value = float(min(hyear_datas[1]))
                hyear_water = (today_value - hyear_min_value) / (hyear_base_value - hyear_min_value)
            hyear_water = round(hyear_water, 4)
        else:
            hyear_water = -1000
        return {'Hwater': hyear_water, 'water': year_water}

    def getWorth_infor1(self, fscode):  # 根据Ｕrl返回请的文本，格式是字典类型。　
        # 同花顺上的单只基金页面信息
        url = 'http://fund.10jqka.com.cn/data/client/myfund/' + fscode
        content = requests.get(url, headers=self.headers).text  # str类型
        jscontent = json.loads(content)
        rawdata = jscontent['data'][0]
        return rawdata

    def getWorth_Valuation_forList(self, query_list):  # 获取care_list的估值信息，格式是字典类型。
        # 基金估值、获取基金当日涨幅情况
        url = 'http://fund.ijijin.cn/data/Net/gz/all_priceRate_desc_0_0_1_9999_0_0_0_jsonp_g.html'
        content = requests.get(url, headers=self.headers).text  # str类型
        # 提取文本有效信息
        content_ = content[2:-1]
        jscontent = json.loads(content_)
        rawdata = jscontent['data']  #
        raw_data = pd.DataFrame(rawdata)
        out_put = pd.DataFrame()
        for i in tqdm(range(len(query_list))):
            code = query_list[i]
            fscode = 'f' + code
            try:
                out_put[code] = raw_data[fscode]
            except Exception as e:
                print(e)
                out_put[code] = math.nan  # 置为空
        return out_put.transpose()

    def getInfo_fromApp(self, fscode):  # 从天天基金的ａｐｐ上抓取的　　　返回字典
        # url = 'https://j5.dfcfw.com/sc/tfs/qt/v2.0.1/110003.json?rand=1621596866760'
        url = 'https://j5.dfcfw.com/sc/tfs/qt/v2.0.1/' + fscode + '.json'
        content = requests.get(url, headers=self.headers).text
        data1 = json.loads(content)  # str类型
        All_INFO = {}
        JJXQ = data1["JJXQ"]["Datas"]
        JJJL = data1['JJJL']["Datas"][0]
        JJJLNEW = data1['JJJLNEW']["Datas"][0]
        JJCC = data1['JJCC']["Datas"]
        JDZF = data1['JDZF']["Datas"]
        # All_INFO['产品特色']=JJXQ['COMMENTS']
        # All_INFO['单位净值']=JJXQ['DWJZ']

        # All_INFO['成立日期']=JJXQ['ESTABDATE']
        # All_INFO['基金规模']=JJXQ['ENDNAV']
        # All_INFO['日涨幅(%)']=JJXQ['RZDF']
        # All_INFO['累计净值']=JJXQ['LJJZ']
        # All_INFO['近1周涨幅(%)']=JDZF[0]['syl']
        # All_INFO['近1月涨幅(%)']=JDZF[1]['syl']
        # All_INFO['近3月涨幅(%)']=JDZF[2]['syl']
        # All_INFO['近6月涨幅(%)']=JDZF[3]['syl']
        # All_INFO['近1年涨幅(%)']=JDZF[4]['syl']
        # All_INFO['近2年涨幅(%)']=JDZF[5]['syl']
        # All_INFO['近3年涨幅(%)']=JDZF[6]['syl']
        All_INFO['fyear'] = JDZF[7]['syl']
        All_INFO['startZF'] = JDZF[9]['syl']
        All_INFO['JJType'] = JJXQ['FTYPE']  # 股票指数
        All_INFO['HC'] = JJXQ['MAXRETRA1']
        All_INFO['XP'] = JJXQ['SHARP1']
        All_INFO['BD'] = JJXQ['STDDEV1']
        if All_INFO['HC'] == '--': All_INFO['HC'] = math.nan
        if All_INFO['XP'] == '--': All_INFO['XP'] = math.nan
        if All_INFO['BD'] == '--': All_INFO['BD'] = math.nan
        # All_INFO['RZDF'] = JJXQ['RZDF']
        All_INFO['DWJZ'] = JJXQ['DWJZ']
        All_INFO['Today'] = JJXQ['FSRQ']
        All_INFO['RISKLEVEL'] = JJXQ['RISKLEVEL']

        # All_INFO['基金经理']=JJJL['MGRNAME']
        All_INFO['manageHBL'] = JJJL['PENAVGROWTH']
        All_INFO['startManage'] = JJJL['FEMPDATE']
        All_INFO['manageDay'] = JJJL['DAYS']
        All_INFO['workDay'] = JJJLNEW['MANGER'][0]['TOTALDAYS']
        All_INFO['yearHBL'] = JJJLNEW['MANGER'][0]['YIELDSE']
        All_INFO['JLlevel'] = JJJLNEW['MANGER'][0]['HJ_JN']
        # All_INFO['定投近１年收益(%)']=JJXQ['PTDT_Y'] #暂时把定投数据关闭
        # All_INFO['定投近２年收益(%)']=JJXQ['PTDT_TWY']
        # All_INFO['定投近３年收益(%)']=JJXQ['PTDT_TRY']
        try:
            All_INFO['GPstock'] = JJCC['InverstPosition']['fundStocks'][0]['GPJC'] + ',' + \
                                  JJCC['InverstPosition']['fundStocks'][1]['GPJC'] + ',' + \
                                  JJCC['InverstPosition']['fundStocks'][2]['GPJC']
        except Exception as e:
            print(e)
            All_INFO['GPstock'] = ''
        # df = pd.DataFrame(All_INFO)
        # print(0)
        return All_INFO

    def getManagerScore(self, df):  # 单独把基金经理的水平算出来
        data = df
        comp = pd.DataFrame()
        comp['manageHBL'] = pd.Series(map(startHBLScore, data['manageHBL']))
        comp['workDay'] = pd.Series(map(workdaysScore, data['workDay']))
        comp['yearHBL'] = pd.Series(map(yearHBLScore, data['yearHBL']))
        # sum score
        comp['score'] = (comp['manageHBL'] + comp['workDay'] + comp['yearHBL']) / 3
        return comp['score']

    def StartFund_select(self, df):  # 通过硬性指标筛选好基金。
        data = df
        comp = pd.DataFrame()

        def Stand_1(size, tyearZF, HC, XP, BD, FR_tyear, FR_year, FR_hyear):
            if isGood(size, 1, 20) and isGood(tyearZF, 1, 80) and isGood(HC, 0, 25) and isGood(
                    XP, 1, 1.5) and isGood(BD, 0, 30) and isGood(FR_tyear, 1, 80) and isGood(FR_year, 1, 80) and isGood(
                FR_hyear, 1, 60):
                return 1
            else:
                return 0

        def Stand_2(size, tyearZF, HC, XP, FR_year):
            if isGood(size, 1, 20) and isGood(tyearZF, 1, 80) and isGood(HC, 0,
                                                                         25) and isGood(
                XP, 1, 1.5) and isGood(FR_year, 1, 80):
                return 1
            else:
                return 0

        def STABLE_1(HC, BD):  # 在稳定波动和回测的情况下，涨幅越大越好
            if isGood(HC, 0, 10) and isGood(BD, 0, 20):
                return 1
            else:
                return 0

        def STABLE_2(HC, BD):  # 在稳定波动和回测的情况下，涨幅越大越好
            if isGood(HC, 0, 20) and isGood(BD, 0, 25):
                return 1
            else:
                return 0

        def EXCITED_1(HC, BD, tyearZF):  # 激进
            if isGood(HC, 1, 25) and isGood(BD, 1, 30) and isGood(tyearZF, 1, 150):
                return 1
            else:
                return 0

        def EXCITED_2(HC, BD, tyearZF):  # 激进
            if isGood(HC, 1, 20) and isGood(BD, 1, 25) and isGood(tyearZF, 1, 100):
                return 1
            else:
                return 0

        comp['STA_1'] = pd.Series(
            map(Stand_1, data['asset'], data['tyear'], data['HC'], data['XP'], data['BD'],
                data['FR_tyear'], data['FR_year'], data['FR_hyear']))
        comp['STA_2'] = pd.Series(
            map(Stand_2, data['asset'], data['tyear'], data['HC'], data['XP'],
                data['FR_year']))
        comp['STB_1'] = pd.Series(map(STABLE_1, data['HC'], data['BD']))
        comp['STB_2'] = pd.Series(map(STABLE_2, data['HC'], data['BD']))
        comp['EXC_1'] = pd.Series(map(EXCITED_1, data['HC'], data['BD'], data['tyear']))
        comp['EXC_2'] = pd.Series(map(EXCITED_2, data['HC'], data['BD'], data['tyear']))
        return comp

    def getFundScore(self, raw_data):  # 单独计算基金的指标
        data = raw_data
        FR = pd.DataFrame()
        FR_list = ['FR_tyear', 'FR_year', 'FR_hyear', 'FR_month']
        FR['score'] = pd.Series(np.zeros(len(data)))
        for name in FR_list:
            FR[name] = pd.Series(map(FRScore, data[name]))
            # FR[name] = data[name]/100.0
            FR['score'] = FR['score'] + FR[name]
        FR['score'] = FR['score'] / len(FR_list)

        JJScore = pd.DataFrame()  # 存储中间变量

        # consider asset\ clrq\ tyearZF,xp,FR. 将数据全部归一化。
        def Nor_tyearZF(one): return one / 300.0 if one < 300 else 1

        def Nor_xp(one): return one / 4.0 if one < 4 else 1

        def Nor_hc(one): return one / 40.0 if one < 40 else 1

        def Nor_bd(one): return one / 40.0 if one < 40 else 1

        JJScore['tyearZF'] = pd.Series(map(Nor_tyearZF, data['tyear']))
        JJScore['HC'] = pd.Series(map(Nor_hc, data['HC']))  # 回测校准
        JJScore['XP'] = pd.Series(map(Nor_xp, data['XP']))
        JJScore['BD'] = pd.Series(map(Nor_bd, data['BD']))
        JJScore['FR'] = FR['score']
        JJScore['S_JL'] = round(pd.Series(self.getManagerScore(raw_data)), 2)
        JJScore['Score'] = round(JJScore['tyearZF'] + JJScore['XP'] * 3 + JJScore['FR'] * 2 + JJScore['S_JL'], 2)

        Out = pd.DataFrame()
        Out['Score'] = JJScore['Score']

        return Out  # 只想返回这一个值

        # print(0)


if __name__ == "__main__":
    FM = Fund_manager()
    FM.Runscore('zhaojing')
    # print(FM.getRZDF('163406'))
