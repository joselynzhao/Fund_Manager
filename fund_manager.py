#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/5/21 下午3:59
# @Author  : Joselynzhao
# @Email   : zhaojing17@forxmail.com
# @File    : fund_manager.py
# @Software: PyCharm
# @Desc    :

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
from Codes_infor import  *

# http://fund.eastmoney.com/005296.html
# url1 = 'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&secids=1.000001,0.399001&invt=2&fields=f2,f3,f4,f6,f12,f104,f105,f106&ut=267f9ad526dbe6b0262ab19316f5a25b&cb=jQuery18307458225946461923_1621588092653&_=1621588092705'
'''
0 上证指数　ｆ104涨　
'''



class Fund_manager():
    def __init__(self, care_list):
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        date = t.split(' ')[0]
        self.date = date
        self.care_list = care_list
        self.headers = {'User-Agent': random.choice(user_agent_list), 'Referer': referer_list[0]}  # 每次运行的时候都会重新生成头部

    def getUrl(self, fscode):  # 同花顺查询单只基金固定信息
        try:
            return 'http://fund.10jqka.com.cn/data/client/myfund/' + fscode
        except Exception as e:
            print(e)
            code = str(fscode)  # 转换为ｓｔｒ格式
            return 'http://fund.10jqka.com.cn/data/client/myfund/' + code

    def getFourRank(self, fscode):  # 获得四分位排名
        url = ''
        try:
            url = 'http://fund.10jqka.com.cn/ifindRank/quarter_year_' + fscode + '.json'
        except Exception as e:
            print(e)
            code = str(fscode)  # 转换为ｓｔｒ格式
            url = 'http://fund.10jqka.com.cn/ifindRank/quarter_year_' + code + '.json'
        content = requests.get(url, headers=self.headers).text  # str类型
        jscontent = json.loads(content)
        results = {}
        try:
            rawdata = jscontent['nowCommonTypeRank']
        except Exception as e:
            print(e)
            return results
        title = ['fyear', 'tyear', 'twoyear', 'year', 'nowyear', 'hyear', 'tmonth', 'month', 'week']
        for name in title:
            try:
                results['FR_' + name] = rawdata[name][2]
            except Exception as e:
                results['FR_' + name] = math.nan
        return results

    def getDWJZ(self, fscode):  # 单位净值数据
        url = 'http://fund.10jqka.com.cn/163406/json/jsondwjz.json'  # 单位净值数据、
        url = 'http://fund.10jqka.com.cn/163406/json/jsonljjz.json'  # 累计净值数据、
        url = 'http://fund.10jqka.com.cn/163406/json/jsonfqjz.json'  # 收益
        try:
            url = 'http://fund.10jqka.com.cn/ifindRank/quarter_year_' + fscode + '.json'
        except Exception as e:
            print(e)
            code = str(fscode)  # 转换为ｓｔｒ格式
            url = 'http://fund.10jqka.com.cn/ifindRank/quarter_year_' + code + '.json'

    def getWorth_infor1(self, fscode):  # 根据Ｕrl返回请的文本，格式是字典类型。　
        # 同花顺上的单只基金页面信息
        url = ''
        try:
            url = 'http://fund.10jqka.com.cn/data/client/myfund/' + fscode
        except Exception as e:
            print(e)
            code = str(fscode)  # 转换为ｓｔｒ格式
            url = 'http://fund.10jqka.com.cn/data/client/myfund/' + code
        content = requests.get(url, headers=self.headers).text  # str类型
        jscontent = json.loads(content)
        rawdata = jscontent['data'][0]
        return rawdata

    def getWorth_Valuation_forOne(self, fscode):  # 获取指定基金编号的估值信息，格式是字典类型。
        # 基金估值、获取基金当日涨幅情况
        url = 'http://fund.ijijin.cn/data/Net/gz/all_priceRate_desc_0_0_1_9999_0_0_0_jsonp_g.html'
        content = requests.get(url, headers=self.headers).text  # str类型
        # 提取文本有效信息
        content_ = content[2:-1]
        jscontent = json.loads(content_)
        rawdata = jscontent['data']  #
        try:
            rawdata = rawdata['f' + fscode]
            return rawdata
        except Exception as e:
            print(e)
            # 对异常情况的处理
            out = {}
            return out  # 返回一个字典

    def getWorth_Valuation_forList(self, query_list):  # 获取care_list的估值信息，格式是字典类型。
        # 基金估值、获取基金当日涨幅情况
        url = 'http://fund.ijijin.cn/data/Net/gz/all_priceRate_desc_0_0_1_9999_0_0_0_jsonp_g.html'
        content = requests.get(url, headers=self.headers).text  # str类型
        # 提取文本有效信息
        content_ = content[2:-1]
        jscontent = json.loads(content_)
        rawdata = jscontent['data']  #
        result = {}
        print(f"正在为{self.care_list['name']}爬取第二部分数据……")
        for i in tqdm(range(len(query_list))):
            fscode = query_list[i]
            # for fscode in self.care_list:
            key = 'f' + fscode
            try:
                result[fscode] = rawdata[key]
            except Exception as e:
                print(e)
                # 对异常情况的处理
                result[fscode] = {}
        return result

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
        All_INFO['基金类型'] = JJXQ['FTYPE']  # 股票指数
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
        All_INFO['近5年涨幅(%)'] = JDZF[7]['syl']
        All_INFO['成立以来涨幅(%)'] = JDZF[9]['syl']
        All_INFO['近１年最大回撤(%)'] = JJXQ['MAXRETRA1']
        All_INFO['近１年夏普比率'] = JJXQ['SHARP1']
        All_INFO['近１年波动率(%)'] = JJXQ['STDDEV1']
        # All_INFO['基金经理']=JJJL['MGRNAME']
        All_INFO['任职回报率(%)'] = JJJL['PENAVGROWTH']
        All_INFO['任期起点'] = JJJL['FEMPDATE']
        All_INFO['任期时长'] = JJJL['DAYS']
        All_INFO['从业时长'] = JJJLNEW['MANGER'][0]['TOTALDAYS']
        All_INFO['年均回报率(%)'] = JJJLNEW['MANGER'][0]['YIELDSE']
        All_INFO['基金经理等级'] = JJJLNEW['MANGER'][0]['HJ_JN']
        # All_INFO['定投近１年收益(%)']=JJXQ['PTDT_Y'] #暂时把定投数据关闭
        # All_INFO['定投近２年收益(%)']=JJXQ['PTDT_TWY']
        # All_INFO['定投近３年收益(%)']=JJXQ['PTDT_TRY']
        try:
            All_INFO['股票重仓'] = JJCC['InverstPosition']['fundStocks'][0]['GPJC'] + ',' + \
                               JJCC['InverstPosition']['fundStocks'][1]['GPJC'] + ',' + \
                               JJCC['InverstPosition']['fundStocks'][2]['GPJC']
        except Exception as e:
            print(e)
            All_INFO['股票重仓'] = ''
        # df = pd.DataFrame(All_INFO)
        # print(0)
        return All_INFO

    def updata_Cares_VIP(self):
        query_list = self.care_list['codes']
        infor1 = {}
        print(f"正在为{self.care_list['name']}爬取第一部分数据……")
        for i in tqdm(range(len(query_list))):
            code = query_list[i]
            data1 = self.getWorth_infor1(code)
            infor1[code] = data1
        infor2 = self.getWorth_Valuation_forList(query_list)
        print(f"正在为{self.care_list['name']}爬取第三部分数据……")
        infor3 = {}
        for i in tqdm(range(len(query_list))):
            code = query_list[i]
            data3 = self.getInfo_fromApp(code)
            infor3[code] = data3
        print("正在爬取第四部分数据……")
        infor4 = {}
        for i in tqdm(range(len(query_list))):
            code = query_list[i]
            data4 = self.getFourRank(code)
            infor4[code] = data4
        df1 = pd.DataFrame(infor1)
        df2 = pd.DataFrame(infor2)
        df3 = pd.DataFrame(infor3)
        df4 = pd.DataFrame(infor4)
        df1 = df1.transpose()
        df2 = df2.transpose()
        df3 = df3.transpose()
        df4 = df4.transpose()

        df2 = df2[['code', 'date', 'preprice', 'price', 'priceRate', 'rate']]
        df2[['code']] = df2[['code']].astype(str)
        df1 = df1[['code', 'name', 'asset', 'clrq', 'levelOfRisk', 'manager', 'maxStar', 'net', 'totalnet1', 'orgname',
                   'sgstat',
                   'shstat', 'week', 'month', 'tmonth', 'hyear', 'year', 'tyear']]  # 取出我要用的数据
        df1[['code']] = df1[['code']].astype(str)
        # df3都是中文字段　并且没有code
        # 先合并１２
        results = pd.concat([df1, df2], axis=1, join='outer')
        results = results[
            ['code', 'name', 'asset', 'clrq', 'levelOfRisk', 'manager', 'maxStar', 'orgname', 'sgstat',
             'shstat', 'date', 'preprice', 'price', 'priceRate', 'net', 'rate', 'totalnet1', 'week', 'month', 'tmonth',
             'hyear',
             'year', 'tyear']]
        # 对ｃｏｌ进行重命名
        results.columns = ['编码１', '编码２', '名称', '规模(亿)', '成立时间', '风险等级', '基金经理', '基金评级', '基金公司', '申购状态',
                           '赎回状态', '当前日期', '基金净值', '当日估值', '估值增长(%)', '当日单位净值', '日增长率-收盘(%)', '累计净值1', '近1周涨幅(%)',
                           '近1月涨幅(%)',
                           '近3月涨幅(%)', '近6月涨幅(%)', '近1年涨幅(%)', '近3年涨幅(%)']

        results_Vip = pd.concat([results, df3, df4], axis=1, join='outer')
        # 调整columns顺序　和选择
        results_Vip = results_Vip[
            ['编码１', '名称', '基金类型', '风险等级', '股票重仓', '基金经理', '任期起点', '基金公司', '规模(亿)', '成立时间', '任职回报率(%)', '任期时长',
             '从业时长', '年均回报率(%)', '基金经理等级', '基金评级', '近3年涨幅(%)', '近5年涨幅(%)', '成立以来涨幅(%)', '近１年最大回撤(%)', '近１年夏普比率',
             '近１年波动率(%)', 'FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year', 'FR_nowyear', 'FR_hyear', 'FR_tmonth',
             'FR_month', 'FR_week', '近1周涨幅(%)', '近1月涨幅(%)',
             '近3月涨幅(%)', '近6月涨幅(%)', '近1年涨幅(%)', '申购状态', '赎回状态', '当前日期', '基金净值', '当日估值', '估值增长(%)', '当日单位净值',
             '日增长率-收盘(%)', '累计净值1']]

        # 写入数据到文件
        try:
            results_Vip.to_excel(f'Infors/信息汇总_{self.care_list["name"]}_{self.date}.xlsx', '信息', index=None, encoding='utf-8')
        except Exception as e:
            print(e)
        # print(0)

        # results_Vip['score'] = self.comp_Score(df)

    def getManagerScore(self,df):  # 单独把基金经理的水平算出来
        # df = pd.read_excel(f'Infors/信息汇总_{self.care_list["name"]}_{self.date}.xlsx')
        datas = df
        data = datas[['编码１', '任职回报率(%)', '任期时长',
                      '从业时长', '年均回报率(%)', ]]
        data.columns = ['code', 'startHBL', 'managedays', 'workdays', 'yearHBL']
        # data.apply(pd.to_numeric)
        comp = pd.DataFrame()
        comp['startHBL'] = pd.Series(map(startHBLScore, data['startHBL']))
        comp['workdays'] = pd.Series(map(workdaysScore, data['workdays']))
        comp['yearHBL'] = pd.Series(map(yearHBLScore, data['yearHBL']))
        # sum score
        comp['score'] = (comp['startHBL'] + comp['workdays'] + comp['yearHBL']) / 3
        return comp['score']

    def StartFund_select(self,df):  # 通过硬性指标筛选好基金。
        # df = pd.read_excel(f'Infors/信息汇总_{self.care_list["name"]}_{self.date}.xlsx')
        datas = df
        data = datas[['编码１', '规模(亿)', '成立时间', '近3年涨幅(%)', '近１年最大回撤(%)',
                      '近１年夏普比率',
                      '近１年波动率(%)', 'FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year', 'FR_nowyear', 'FR_hyear',
                      'FR_tmonth', 'FR_month', 'FR_week', '基金净值', '累计净值1']]
        data.columns = ['code', 'size', 'startTime', 'tyearZF', 'HC', 'XP', 'BD', 'FR_fyear', 'FR_tyear', 'FR_twoyear',
                        'FR_year',
                        'FR_nowyear', 'FR_hyear', 'FR_tmonth', 'FR_month', 'FR_week', 'DWJZ', 'LJJZ']
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

        comp['stand_1'] = pd.Series(
            map(Stand_1, data['size'], data['tyearZF'], data['HC'], data['XP'], data['BD'],
                data['FR_tyear'], data['FR_year'], data['FR_hyear']))
        comp['stand_2'] = pd.Series(
            map(Stand_2, data['size'], data['tyearZF'], data['HC'], data['XP'],
                data['FR_year']))
        comp['STABLE_1'] = pd.Series(map(STABLE_1, data['HC'], data['BD']))
        comp['STABLE_2'] = pd.Series(map(STABLE_2, data['HC'], data['BD']))
        comp['EXCITED_1'] = pd.Series(map(EXCITED_1, data['HC'], data['BD'], data['tyearZF']))
        comp['EXCITED_2'] = pd.Series(map(EXCITED_2, data['HC'], data['BD'], data['tyearZF']))
        return comp

    def getFundScore(self):  # 单独计算基金的指标
        raw_data = pd.read_excel(f'Infors/信息汇总_{self.care_list["name"]}_{self.date}.xlsx')
        datas = raw_data
        df=raw_data
        data = datas[['编码１', '规模(亿)', '成立时间', '近3年涨幅(%)', '近１年最大回撤(%)',
                      '近１年夏普比率',
                      '近１年波动率(%)', 'FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year', 'FR_nowyear', 'FR_hyear',
                      'FR_tmonth', 'FR_month', 'FR_week', '基金净值', '累计净值1']]
        data.columns = ['code', 'size', 'startTime', 'tyearZF', 'HC', 'XP', 'BD', 'FR_fyear', 'FR_tyear', 'FR_twoyear',
                        'FR_year',
                        'FR_nowyear', 'FR_hyear', 'FR_tmonth', 'FR_month', 'FR_week', 'DWJZ', 'LJJZ']

        FR = pd.DataFrame()
        FR_list = ['FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year', 'FR_nowyear', 'FR_hyear', 'FR_tmonth', 'FR_month',
                   'FR_week']

        FR['score'] = pd.Series(np.zeros(len(data)))
        for name in FR_list:
            FR[name] = pd.Series(map(FRScore, data[name]))
            FR['score'] = FR['score'] + FR[name]
        FR['score'] = FR['score'] / len(FR_list)

        comp = pd.DataFrame()
        comp['tyearZF'] = pd.Series(map(tyearZFScore, data['tyearZF']))
        comp['HC'] = pd.Series(map(HC_justScore, data['tyearZF'], data['HC']))  # 回测校准
        comp['XP'] = pd.Series(map(XPScore, data['XP']))
        comp['BD'] = pd.Series(map(BDScore, data['BD']))
        comp['FR'] = FR['score']

        HC = pd.Series(map(HCScore, data['HC']))  # 标准回测
        df['Score1'] = (comp['tyearZF'] + comp['HC'] + comp['XP'] + comp['BD'] + comp['FR']) / 5
        df['Score2'] = (comp['XP'] + comp['tyearZF'] + comp['FR']) / 3
        df['Score3'] = (comp['XP'] + comp['tyearZF'] + comp['FR'] - HC - comp['BD'])
        df['经理得分'] = pd.Series(self.getManagerScore(raw_data))
        df = pd.concat([df, self.StartFund_select(raw_data)], axis=1, join="outer")
        df = df[
            ['编码１', '名称', '基金类型', '风险等级', '股票重仓', '基金经理', '基金经理等级', '经理得分', '基金评级', 'Score1', 'Score2', 'Score3', 'stand_1',
             'stand_2','STABLE_1','STABLE_2','EXCITED_1','EXCITED_2','近3年涨幅(%)','累计净值1','近1周涨幅(%)','近1月涨幅(%)','近3月涨幅(%)','近6月涨幅(%)','基金净值','当日估值','估值增长(%)','当日单位净值','日增长率-收盘(%)']]

        makeRound2_list = ['经理得分','Score1', 'Score2', 'Score3']
        def keepFloat2(one):
            return round(one,2)
        for name in makeRound2_list:
            df[name] = pd.Series(map(keepFloat2,df[name]))
            # df[name] = pd.Series(map(round,df[name],2))
        # 写入数据到文件
        try:

            df.to_excel(f'Scores/{self.care_list["name"]}_{self.date}.xlsx', '信息', index=None, encoding='utf-8')
        except Exception as e:
            print(e)
        print(0)

    def comp_Score_number(self):
        df = pd.read_excel(f'Infors/信息汇总_{self.care_list["name"]}.xlsx')
        datas = df
        data = datas[['编码１', '规模(亿)', '任职回报率(%)', '任期时长',
                      '从业时长', '年均回报率(%)', '基金经理等级', '基金评级', '近3年涨幅(%)', '近１年最大回撤(%)',
                      '近１年夏普比率',
                      '近１年波动率(%)', 'FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year', 'FR_nowyear', 'FR_hyear',
                      'FR_tmonth', 'FR_month', 'FR_week', '基金净值', '累计净值1']]
        data.columns = ['code', 'size', 'startHBL', 'managedays', 'workdays', 'yearHBL', 'JLlevel',
                        'JJlevel', 'tyearZF', 'HC', 'XP', 'BD', 'FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year',
                        'FR_nowyear', 'FR_hyear', 'FR_tmonth', 'FR_month', 'FR_week', 'DWJZ', 'LJJZ']
        # data.apply(pd.to_numeric)
        comp = pd.DataFrame()

        FR = pd.DataFrame()
        FR_list = ['FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year', 'FR_nowyear', 'FR_hyear', 'FR_tmonth', 'FR_month',
                   'FR_week']

        FR['score'] = pd.Series(np.zeros(len(data)))
        for name in FR_list:
            FR[name] = pd.Series(map(FRScore, data[name]))
            FR['score'] = FR['score'] + FR[name]
        FR['score'] = FR['score'] / len(FR_list)

        comp['size'] = pd.Series(map(sizeScore, data['size']))
        comp['startHBL'] = pd.Series(map(startHBLScore, data['startHBL']))
        comp['workdays'] = pd.Series(map(workdaysScore, data['workdays']))
        comp['JLlevel'] = pd.Series(map(JLlevelScore, data['JLlevel']))
        comp['JJlevel'] = pd.Series(map(JJlevelScore, data['JJlevel']))
        comp['tyearZF'] = pd.Series(map(tyearZFScore, data['tyearZF']))
        # comp['HC'] = pd.Series(map(HCScore, data['HC']))
        comp['HC'] = pd.Series(map(HC_justScore, data['tyearZF'], data['HC']))  # 回测校准
        comp['XP'] = pd.Series(map(XPScore, data['XP']))
        comp['BD'] = pd.Series(map(BDScore, data['BD']))
        comp['FR'] = FR['score']
        comp['JZ'] = pd.Series(map(DWJZ_LJJZScore, data['DWJZ'], data['LJJZ']))

        col = comp.columns.tolist()

        QZ_set = {
            'qz1': [0.2, 1, 1.5, 0.3, 1.5, 0.7, 0.8, 1, 1, 2, 2, 2],
            'qz2': [1] * len(comp),
            'qz3': [1, 1, 3, 2, 2, 7, 4, 7, 3, 5, 3],
            '长期投资得分': [1, 2, 1, 2, 2, 4, 0.5, 1, 0.5, 3, 3],  # 3年及以上投资期限，以半年为操作单位
            '中期投资得分': [1, 1, 1, 1.5, 2, 1, 1.5, 2, 1.5, 2, 3],  # 1~3年投资期限，以月为操作单位
            '短期投资得分': [0.5, 1, 0.5, 1, 2, 0.5, 2, 2, 2, 2, 3],  # 1年投资期限，以周为操作单

        }
        Use_QZ_name_list = ['长期投资得分', '中期投资得分', '短期投资得分']
        # Score_set = {}
        for QZ_name in Use_QZ_name_list:
            QZ = QZ_set[QZ_name]  # 得到权重列表
            QZZ = sum(QZ)
            score = [0] * len(comp)
            # score = pd.Series(score_)
            for i in range(len(comp)):
                for j in range(len(col)):
                    col_name = col[j]
                    data_a = comp[col_name][i]
                    data_b = QZ[j]
                    score[i] = score[i] + data_a * data_b
                score[i] = score[i] / QZZ
            df[QZ_name] = pd.Series(score)
        df = df[
            ['编码１', '名称', '基金类型', '风险等级', '股票重仓', '基金经理', '规模(亿)', '任职回报率(%)', '任期时长',
             '从业时长', '年均回报率(%)', '基金经理等级', '基金评级', '近3年涨幅(%)', '近１年最大回撤(%)',
             '近１年夏普比率',
             '近１年波动率(%)', '长期投资得分', '中期投资得分', '短期投资得分']]
        # 写入数据到文件
        try:
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(t)
            df.to_excel(f'Scores/{self.care_list["name"]}_{t}.xlsx', '信息', index=None, encoding='utf-8')
        except Exception as e:
            print(e)
        print(0)

    def comp_Score(self, file_name):  # 比例行
        df = pd.read_excel(f'Infors/{file_name}.xlsx')

        # datas = pd.read_excel("OUTPUTS/基金关注_2021-05-22 14:32:16.xlsx")
        datas = df
        # 提取用于计算评分的数据
        data = datas[['编码２', '规模(亿)', '任职回报率(%)', '任期时长',
                      '从业时长', '年均回报率(%)', '基金经理等级', '基金评级', '近3年涨幅(%)', '近5年涨幅(%)', '成立以来涨幅(%)', '近１年最大回撤(%)',
                      '近１年夏普比率',
                      '近１年波动率(%)']]

        # length = len(data)
        # col = data.columns.tolist()
        data.columns = ['code', 'size', 'startHBL', 'managedays', 'workdays', 'yearHBL', 'JLlevel',
                        'JJlevel', 'tyearZF', 'fyearZF', 'startZF', 'HC', 'XP', 'BD']

        # 转换数据类型
        # tran_data = np.array(data,dtype=np.float)
        # data = pd.DataFrame(tran_data)
        # for col in data.columns.tolist():
        #     for i in range(len(data)):
        #         value = data[col][i]
        #         if math.isnan(data[col][i]):
        #             data[col][i] = 0
        #     data[col] = data[col].apply(pd.to_numeric)
        # data[col] = pd.to_numeric(data[col],errors = 'coerce')
        # data[col] = data[col].apply(lambda x: float(x) if math.isnan(x) else 0)

        # data[['code', 'size', 'startHBL', 'managedays', 'workdays', 'yearHBL', 'JLlevel',
        #                 'JJlevel', 'tyearZF', 'fyearZF', 'startZF', 'HC', 'XP', 'BD']].apply(lambda  x:float(x) if math.isnan(x) else 0)
        # except Exception as e:
        #     print(e)
        # data['size'].apply(pd.to_numeric)
        # data['comp'] = data['workdays'] - data['managedays']
        # describe = data.describe()

        # size_min = data['size'].min()
        # size_max = data['size'].max()
        # size_mean = data['size'].mean()
        # size_sum = data['size'].sum()
        comp = pd.DataFrame()
        # test = v_datas['从业时长'].append(0)

        size_stand = 50

        def size_just(one):
            return abs(size_stand - float(one))

        size_ = list(map(size_just, data['size']))
        size_min = pd.Series(size_).min()
        size_max = pd.Series(size_).max()

        def getSizeScore(one_size):
            return 1 - (abs(one_size - size_stand) - size_min) / (size_max - size_min)

        comp['sizeScore'] = list(map(getSizeScore, data['size']))

        # 以任期时长作为　任职回报率 和　年均回报率　的可信度
        # 归一化任期时长
        def Nor_managedays(one):
            return (one - 0) / (data['managedays'].max() - 0)

        managedays_ = pd.Series(map(Nor_managedays, data['managedays']))

        def Nor_workdays(one):
            return (one - 0) / (data['workdays'].max() - 0)

        workdays_ = pd.Series(map(Nor_workdays, data['workdays']))
        # 归一话任期回报率

        StartHBL = data['startHBL'] * managedays_

        def Nor_startHBL(one):
            return (one - 0) / (StartHBL.max() - 0)

        startHBL_ = pd.Series(map(Nor_startHBL, StartHBL))
        comp['startHBLScore'] = startHBL_  # 待核查　是不是对应位置相加

        yearHBL = workdays_ * data['yearHBL']

        def Nor_yearHBL(one):
            return (one - 0) / (yearHBL.max() - 0)

        yearHBL_ = pd.Series(map(Nor_yearHBL, yearHBL))
        comp['yearHBLScore'] = yearHBL_
        comp['workdaysScore'] = workdays_

        def Nor_JLlevel(one):
            return (one - 0) / (data['JLlevel'].max() - 0)

        comp['JLlevelScore'] = pd.Series(map(Nor_JLlevel, data['JLlevel']))

        def Nor_JJlevel(one):
            return (one - 0) / (data['JJlevel'].max() - 0)

        comp['JJlevelScore'] = pd.Series(map(Nor_JJlevel, data['JJlevel']))

        def Nor_HC(one):
            return 1 - (one - data['HC'].min()) / (data['HC'].max() - data['HC'].min())

        comp['HCScore'] = pd.Series(map(Nor_HC, data['HC']))

        def Nor_BD(one):
            return 1 - (one - data['BD'].min()) / (data['BD'].max() - data['BD'].min())

        comp['BDScore'] = pd.Series(map(Nor_BD, data['BD']))

        def Nor_XP(one):
            return (one - data['XP'].min()) / (data['XP'].max() - data['XP'].min())

        comp['XPScore'] = pd.Series(map(Nor_XP, data['XP']))

        def Nor_tyearZF(one):
            return (one - data['tyearZF'].min()) / (data['tyearZF'].max() - data['tyearZF'].min())

        comp['tyearZFScore'] = pd.Series(map(Nor_tyearZF, data['tyearZF']))

        for i in range(len(comp)):  # 处理ｎａｎ的问题
            # value = comp['JJlevelScore'][i]
            if math.isnan(comp['JJlevelScore'][i]):
                # print('yes')
                comp['JJlevelScore'][i] = 0
        # comp['JJlevelScore'] = pd.Series(map(check_nan,comp['JJlevelScore']))
        col = comp.columns.tolist()
        # ['sizeScore', 'startHBLScore', 'yearHBLScore', 'workdaysScore', 'JLlevelScore', 'JJlevelScore',
        #                 'HCScore', 'BDScore', 'XPScore', 'tyearZFScore']
        qz1 = [0.2, 1, 1.5, 0.3, 1.5, 0.7, 0.8, 1, 1, 2]
        qz2 = [1, 5, 3, 3, 4, 4, 5, 5, 9, 9]
        QZ = qz2
        QZZ = sum(QZ)
        score = [0] * len(comp)
        # score = pd.Series(score_)
        for i in range(len(comp)):
            for j in range(len(col)):
                col_name = col[j]
                data_a = comp[col_name][i]
                data_b = QZ[j]
                score[i] = score[i] + data_a * data_b
            score[i] = score[i] / QZZ

        # comp['final_Score'] = (0.2*comp['sizeScore'] + 1*comp['startHBLScore'] + 1.5*comp['yearHBLScore'] + 0.3*comp[
        #     'workdaysScore'] + 1.5*comp[
        #                            'JLlevelScore'] + 0.7* comp['HCScore'] + 0.8*comp['BDScore'] + 1* comp['XPScore'] + 1 *comp[
        #                            'JJlevelScore'] + 2 * comp['tyearZFScore']) / 11

        # return comp['final_Score']
        df['score'] = pd.Series(score)
        df = df[['编码１', '名称', '基金类型', '风险等级', '股票重仓', '基金经理', 'score', '近1周涨幅(%)', '近1月涨幅(%)',
                 '近3月涨幅(%)', '近6月涨幅(%)', '近1年涨幅(%)', '当前日期', '基金净值', '当日估值', '估值增长(%)', '当日单位净值',
                 '日增长率-收盘(%)']]
        # 写入数据到文件
        try:
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(t)
            df.to_excel(f'OUTPUTS/{file_name}_{t}.xlsx', '信息', index=None, encoding='utf-8')
        except Exception as e:
            print(e)
        print(0)

    def SummarizeAllList(self,list_lsit): # 传入的是list的一个list
        Score_Sum = pd.DataFrame()
        # Infor_Sum = pd.DataFrame()
        for list_name in list_lsit:
            infor = pd.read_excel(f'Scores/{list_name["name"]}_{self.date}.xlsx')
            belong = pd.Series([list_name['name']]*len(infor))
            infor.insert(0,'来源',belong)
            Score_Sum = pd.concat([Score_Sum,infor],axis=0,join='outer')
        Score_Sum.sort_values(by='Score1',inplace=True,ascending =False)  # sort
        try:
            Score_Sum.to_excel(f'Scores/汇总_{self.date}.xlsx', '信息', index=None, encoding='utf-8')
        except Exception as e:
            print(e)

if __name__ == "__main__":
    all_list = [care_list_zj,care_list_dd1,care_list_dd2,guanwang_zj]

    # FM = Fund_manager(guanwang_zj)
    # FM.updata_Cares_VIP()
    # FM.comp_Score_number()
    # FM.getFundScore() #得到各种分数，稳定？　激进？
    # FM.SummarizeAllList(all_list) # 把所有分数信息来合成一张表

    # 每日更新内容
    for cares in all_list:
        FM = Fund_manager(cares)
        FM.updata_Cares_VIP() # 更新数据
        FM.getFundScore()# #得到各种分数，稳定？　激进？
    FM_s = Fund_manager(care_list_zj)## 把所有分数信息来合成一张表
    FM_s.SummarizeAllList(all_list)


