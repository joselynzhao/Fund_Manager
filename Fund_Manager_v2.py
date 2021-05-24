#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/5/24 下午7:25
# @Author  : Joselynzhao
# @Email   : zhaojing17@forxmail.com
# @File    : Fund_Manager_v2.py
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
from Codes_infor import *

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

    def Runscore(self, col_list):  # 制定跑哪几列分数
        codes = pd.read_excel('codes.xlsx', dtype=str)  # 全部读取为字符串格式

        def get_col_code_len(col_codes):
            i = 0
            for one in col_codes:
                try:
                    math.isnan(one)
                    break
                except Exception as e:
                    i = i + 1
            return i

        get_Infors = pd.DataFrame()
        for col_code_name in col_list:
            # 处理长度　
            col_codes = codes[col_code_name]
            len_col = get_col_code_len(col_codes)
            print(f"正在为【{col_code_name}】爬取数据。")
            for i in tqdm(range(len_col)):
                code = col_codes[i]
                FR = pd.Series(self.getFourRank(code))
                TTJJ = pd.Series(self.getWorth_infor1(code))  # 返回很多信息
                THS = pd.Series(self.getInfo_fromApp(code))
                # 　处理获得的数据
                # FR 和同花顺也不需要处理　全选
                TTJJ = TTJJ[['code', 'name', 'asset', 'clrq', 'levelOfRisk', 'manager', 'maxStar', 'net', 'totalnet1',
                             'orgname', 'week', 'month', 'tmonth', 'hyear', 'year', 'tyear']]
                code_infor = pd.DataFrame()

                code_infor = pd.concat([code_infor, FR, TTJJ, THS], axis=0)
                code_infor.loc['Source'] = col_code_name
                code_infor.columns = [code]
                # get_Infors = get_Infors.append(code_infor,ignore_index=True)
                get_Infors = pd.concat([get_Infors, code_infor], axis=1)
        # 一次行抓取最后一部分数据
        get_Infors = get_Infors.transpose()
        query_list = list(get_Infors['code'])
        value_infor = pd.DataFrame(self.getWorth_Valuation_forList(query_list))
        value_infor = value_infor.transpose()
        value_infor = value_infor[['date', 'preprice', 'price', 'priceRate', 'rate']]
        get_Infors = pd.concat([get_Infors, value_infor], axis=1, join='outer')
        print(get_Infors.columns.tolist())
        try:
            get_Infors.to_excel(f'Infors/信息汇总_{self.date}.xlsx', '信息', index=None, encoding='utf-8')
        except Exception as e:
            print(e)

        # 获取数据评分处理
        raw_data = pd.read_excel(f'Infors/信息汇总_{self.date}.xlsx')
        self.getFundScore(raw_data)

        # print(0)

    # df = pd.read_excel(f'Infors/信息汇总_{self.care_list["name"]}_{self.date}.xlsx')

    def getFourRank(self, fscode):  # 获得四分位排名
        url = ''
        try:
            url = 'http://fund.10jqka.com.cn/ifindRank/quarter_year_' + fscode + '.json'
        except Exception as e:
            print(e)
            code = str(fscode)  # 转换为ｓｔｒ格式
            url = 'http://fund.10jqka.com.cn/ifindRank/quarter_year_' + code + '.json'
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
        # print(f"正在为{self.care_list['name']}爬取第二部分数据……")
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
        All_INFO['JJType'] = JJXQ['FTYPE']  # 股票指数
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
        All_INFO['fyearZF'] = JDZF[7]['syl']
        All_INFO['startZF'] = JDZF[9]['syl']
        All_INFO['HC'] = JJXQ['MAXRETRA1']
        All_INFO['XP'] = JJXQ['SHARP1']
        All_INFO['BD'] = JJXQ['STDDEV1']
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
            results_Vip.to_excel(f'Infors/信息汇总_{self.care_list["name"]}_{self.date}.xlsx', '信息', index=None,
                                 encoding='utf-8')
        except Exception as e:
            print(e)
        # print(0)

        # results_Vip['score'] = self.comp_Score(df)

    def getManagerScore(self, df):  # 单独把基金经理的水平算出来
        # df = pd.read_excel(f'Infors/信息汇总_{self.care_list["name"]}_{self.date}.xlsx')
        data = df
        # data = datas[['编码１', '任职回报率(%)', '任期时长',
        #               '从业时长', '年均回报率(%)', ]]
        # data.columns = ['code', 'startHBL', 'managedays', 'workdays', 'yearHBL']
        # data.apply(pd.to_numeric)
        comp = pd.DataFrame()
        comp['manageHBL'] = pd.Series(map(startHBLScore, data['manageHBL']))
        comp['workDay'] = pd.Series(map(workdaysScore, data['workDay']))
        comp['yearHBL'] = pd.Series(map(yearHBLScore, data['yearHBL']))
        # sum score
        comp['score'] = (comp['manageHBL'] + comp['workDay'] + comp['yearHBL']) / 3
        return comp['score']

    def StartFund_select(self, df):  # 通过硬性指标筛选好基金。
        # df = pd.read_excel(f'Infors/信息汇总_{self.care_list["name"]}_{self.date}.xlsx')
        data = df
        # data = datas[['编码１', '规模(亿)', '成立时间', '近3年涨幅(%)', '近１年最大回撤(%)',
        #               '近１年夏普比率',
        #               '近１年波动率(%)', 'FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year', 'FR_nowyear', 'FR_hyear',
        #               'FR_tmonth', 'FR_month', 'FR_week', '基金净值', '累计净值1']]
        # data.columns = ['code', 'size', 'startTime', 'tyearZF', 'HC', 'XP', 'BD', 'FR_fyear', 'FR_tyear', 'FR_twoyear',
        #                 'FR_year',
        #                 'FR_nowyear', 'FR_hyear', 'FR_tmonth', 'FR_month', 'FR_week', 'DWJZ', 'LJJZ']
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
            map(Stand_1, data['asset'], data['tyear'], data['HC'], data['XP'], data['BD'],
                data['FR_tyear'], data['FR_year'], data['FR_hyear']))
        comp['stand_2'] = pd.Series(
            map(Stand_2, data['asset'], data['tyear'], data['HC'], data['XP'],
                data['FR_year']))
        comp['STABLE_1'] = pd.Series(map(STABLE_1, data['HC'], data['BD']))
        comp['STABLE_2'] = pd.Series(map(STABLE_2, data['HC'], data['BD']))
        comp['EXCITED_1'] = pd.Series(map(EXCITED_1, data['HC'], data['BD'], data['tyear']))
        comp['EXCITED_2'] = pd.Series(map(EXCITED_2, data['HC'], data['BD'], data['tyear']))
        return comp

    def getFundScore(self, raw_data):  # 单独计算基金的指标
        data = raw_data
        # data = datas[['编码１', '规模(亿)', '成立时间', '近3年涨幅(%)', '近１年最大回撤(%)',
        #               '近１年夏普比率',
        #               '近１年波动率(%)', 'FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year', 'FR_nowyear', 'FR_hyear',
        #               'FR_tmonth', 'FR_month', 'FR_week', '基金净值', '累计净值1']]
        # data.columns = ['code', 'size', 'startTime', 'tyearZF', 'HC', 'XP', 'BD', 'FR_fyear', 'FR_tyear', 'FR_twoyear',
        #                 'FR_year',
        #                 'FR_nowyear', 'FR_hyear', 'FR_tmonth', 'FR_month', 'FR_week', 'DWJZ', 'LJJZ']
        FR = pd.DataFrame()
        FR_list = ['FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year', 'FR_nowyear', 'FR_hyear', 'FR_tmonth', 'FR_month',
                   'FR_week']
        FR['score'] = pd.Series(np.zeros(len(data)))
        for name in FR_list:
            FR[name] = pd.Series(map(FRScore, data[name]))
            FR['score'] = FR['score'] + FR[name]
        FR['score'] = FR['score'] / len(FR_list)

        comp = pd.DataFrame()
        comp['tyearZF'] = pd.Series(map(tyearZFScore, data['tyear']))
        comp['HC'] = pd.Series(map(HC_justScore, data['tyear'], data['HC']))  # 回测校准
        comp['XP'] = pd.Series(map(XPScore, data['XP']))
        comp['BD'] = pd.Series(map(BDScore, data['BD']))
        comp['FR'] = FR['score']

        HC = pd.Series(map(HCScore, data['HC']))  # 标准回测
        data['S_JL'] = pd.Series(self.getManagerScore(raw_data))
        data['S_zq'] = (comp['XP'] + comp['HC'] + comp['BD'] + comp['FR'] + data['S_JL'] + comp['tyearZF']) / 6
        data['S_zd'] = (comp['XP'] - comp['HC'] - comp['BD'] + comp['FR'] + data['S_JL'] + comp['tyearZF']) / 2
        data['S_zs'] = (comp['XP'] + comp['HC'] + comp['FR'] + comp['tyearZF']) / 4
        # data['Score1'] = (comp['tyearZF'] + comp['HC'] + comp['XP'] + comp['BD'] + comp['FR']) / 5
        # data['Score2'] = (comp['XP'] + comp['tyearZF'] + comp['FR']) / 3
        # data['Score3'] = (comp['XP'] + comp['tyearZF'] + comp['FR'] - HC - comp['BD'])

        data = pd.concat([data, self.StartFund_select(raw_data)], axis=1, join="outer")
        print(data.columns.tolist())

        # colll =

        data = data[['Source','code','name','levelOfRisk','GPstock','manager', 'JLlevel']]

        # makeRound2_list = ['经理得分', 'Score1', 'Score2', 'Score3']
        def keepFloat2(one):
            return round(one, 2)

        # for name in makeRound2_list:
        #     df[name] = pd.Series(map(keepFloat2, df[name]))
        # df[name] = pd.Series(map(round,df[name],2))
        # 写入数据到文件
        try:

            data.to_excel(f'Scores/汇总_{self.date}.xlsx', '信息', index=None, encoding='utf-8')
        except Exception as e:
            print(e)
        # print(0)


if __name__ == "__main__":
    # all_list = [care_list_zj,care_list_dd1,care_list_dd2,guanwang_zj]

    # FM = Fund_manager(guanwang_zj)
    # FM.updata_Cares_VIP()
    # FM.comp_Score_number()
    # FM.getFundScore() #得到各种分数，稳定？　激进？
    # FM.SummarizeAllList(all_list) # 把所有分数信息来合成一张表

    # # 每日更新内容
    # for cares in all_list:
    #     FM = Fund_manager(cares)
    #     FM.updata_Cares_VIP() # 更新数据
    #     FM.getFundScore()# #得到各种分数，稳定？　激进？
    # FM_s = Fund_manager(care_list_zj)## 把所有分数信息来合成一张表
    # FM_s.SummarizeAllList(all_list)
    FM = Fund_manager()
    FM.Runscore(['测试'])
