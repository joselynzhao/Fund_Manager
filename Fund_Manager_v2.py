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
        # query_list = list(get_Infors['code'])
        # print(query_list)
        # value_infor = pd.DataFrame(self.getWorth_Valuation_forList(query_codes))
        # value_infor = value_infor.transpose()
        # value_infor = value_infor[['preprice', 'price', 'priceRate', 'rate','net']]
        get_Infors = pd.concat([codes_infor, get_Infors], axis=1, join='outer')
        # cols = ['type', 'FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year', 'FR_nowyear', 'FR_hyear', 'FR_tmonth',
        #         'FR_month', 'FR_week', 'code', 'name', 'asset', 'clrq', 'levelOfRisk', 'manager', 'maxStar',
        #         'totalnet1', 'orgname', 'week', 'month', 'tmonth', 'hyear', 'year', 'tyear', 'fyear', 'startZF',
        #         'JJType',   'manageHBL', 'startManage', 'manageDay', 'workDay',
        #         'yearHBL', 'JLlevel', ]

        get_Infors = get_Infors[[
             'code','type', 'name', 'JJType', 'maxStar', 'clrq', 'levelOfRisk', 'manager', 'JLlevel', 'orgname',
            'GPstock',
            'FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year', 'FR_nowyear', 'FR_hyear', 'FR_tmonth', 'FR_month',
            'FR_week',
            'asset', 'totalnet1', 'DWJZ', 'HC', 'XP', 'BD',
            'week', 'month', 'tmonth', 'hyear', 'year', 'tyear', 'fyear', 'startZF',
            'manageHBL', 'yearHBL',
            'manageDay', 'workDay',
            'Hwater', 'water',
        ]]

        print(get_Infors.columns.tolist())

        # 获取数据评分处理
        comp_in = get_Infors[
            ['FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year', 'FR_nowyear', 'FR_hyear', 'FR_tmonth', 'FR_month',
             'FR_week',
             'asset', 'totalnet1', 'DWJZ', 'HC', 'XP', 'BD',
             'week', 'month', 'tmonth', 'hyear', 'year', 'tyear', 'fyear', 'startZF',
             'manageHBL', 'yearHBL', 'manageDay', 'workDay']].apply(pd.to_numeric, errors='ignore')
        # raw_data = pd.read_excel(f'Infors/信息汇总_{self.date}_{input_file_name}.xlsx')
        comp_out = self.getFundScore(comp_in)
        # code_list = get_Infors['code']
        # comp_out['code'] = code_list
        comp_out.set_index(get_Infors['code'], inplace=True)

        # makeRound2_list = ['S_JL','S_zq','S_zd','S_zs']
        # def keepFloat2(one):
        #     return round(one, 2)
        # for name in makeRound2_list:
        #     # comp_out[name] = pd.Series(map(keepFloat2, comp_out[name]))
        #     comp_out[name] = round(comp_out[name],2)
        #     # comp_out[name] = pd.Series(map(lambda x: '%.3f' % x,comp_out[name]))
        # 写入数据到文件
        get_Infors = pd.concat([get_Infors, comp_out], axis=1)
        try:
            get_Infors.to_excel(f'Infors/信息汇总_{self.date}_{input_file_name}.xlsx', '信息', index=None, encoding='utf-8')
        except Exception as e:
            print(e)
        # ALL_INFOR = get_Infors[[
        #     'type', 'code', 'name','JJType','maxStar','clrq', 'levelOfRisk', 'manager','JLlevel', 'orgname','GPstock',
        #     'FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year', 'FR_nowyear', 'FR_hyear', 'FR_tmonth', 'FR_month', 'FR_week',
        #     'asset', 'totalnet1','DWJZ', 'HC', 'XP', 'BD',
        #     'week', 'month', 'tmonth', 'hyear', 'year', 'tyear', 'fyear', 'startZF',
        #     'manageHBL', 'yearHBL',
        #     'manageDay', 'workDay',
        #     'S_JL', 'S_zq', 'S_zd', 'S_zs',
        #     'stand_1','stand_2','STABLE_1','STABLE_2','EXCITED_1','EXCITED_2'
        # ]]
        # get_Infors = pd.read_excel(f'Infors/信息汇总_{self.date}_{input_file_name}.xlsx')

        SCORE = get_Infors[[
            'code','type', 'name', 'JJType', 'maxStar', 'GPstock', 'manager', 'JLlevel', 'S_JL',
            'totalnet1', 'DWJZ', 'HC', 'XP', 'BD',
            'STB_up','EXC_~', 'Hwater', 'water',
            'week', 'month', 'tmonth', 'hyear', 'year', 'tyear', 'fyear',
        ]]
        #　主要是根据根数来看操作
        # OP_In = get_Infors[['JJType', ]]
        # OP = self.getOP()
        try:
            SCORE.to_excel(f'Scores/汇总_{self.date}_{input_file_name}.xlsx', '信息', index=None, encoding='utf-8')
        except Exception as e:
            print(e)


    def SCORE(self,input_file_name):
        get_Infors = pd.read_excel(f'Infors/信息汇总_{self.date}_{input_file_name}.xlsx')

        SCORE = get_Infors[[
            'code', 'type', 'name', 'JJType', 'maxStar', 'GPstock', 'manager', 'JLlevel', 'S_JL',
            'totalnet1', 'DWJZ', 'HC', 'XP', 'BD',
            'STB_up', 'EXC_~', 'Hwater', 'water',
            'week', 'month', 'tmonth', 'hyear', 'year', 'tyear', 'fyear',
        ]]
        # 　主要是根据根数来看操作
        # OP_In = get_Infors[['JJType', ]]
        # OP = self.getOP()
        try:
            SCORE.to_excel(f'Scores/汇总_{self.date}_{input_file_name}.xlsx', '信息', index=None, encoding='utf-8')
        except Exception as e:
            print(e)

        # 试着进行操作指示

    def getOP(self,df):
        pass


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
            if year_max_value !=year_base_value:
                # hyear_max_index = hyear_datas.index(hyear_max_value)
                year_water = (today_value - year_base_value) / (year_max_value - year_base_value)

            else:
                year_min_value = float(min(year_datas[1]))
                year_water = (today_value-year_min_value)/(year_base_value-year_min_value)
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
                hyear_water = (today_value-hyear_min_value)/(hyear_base_value-hyear_min_value)
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

        comp['HC_stan'] = pd.Series(map(HCScore, data['HC']))  # 标准回测
        compOut = pd.DataFrame()
        compOut['S_JL'] = round(pd.Series(self.getManagerScore(raw_data)), 2)
        # compOut['S_zq'] = round(
        #     (comp['XP'] + comp['HC'] * 2 + comp['BD'] + comp['FR'] + compOut['S_JL'] + comp['tyearZF']) / 7, 2)
        # compOut['S_zd'] = round(
        #     (comp['XP'] * 2 - comp['HC'] - comp['BD'] + comp['FR'] + compOut['S_JL'] + comp['tyearZF']) / 3, 2)
        # compOut['S_zs'] = round((comp['XP']*2 + comp['HC'] + comp['FR'] + comp['tyearZF']) / ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc 4, 2)
        compOut['STB_up'] = round((comp['HC_stan']*3 +comp['BD']*2+comp['XP']*2+compOut['S_JL'])/8,2)
        compOut['EXC_~'] = round((comp['XP']*2-comp['HC_stan']-comp['BD']+compOut['S_JL'])/1,2)
        # compOut = pd.concat([compOut, self.StartFund_select(raw_data)], axis=1, join="outer")
        # print(data.columns.tolist())

        # colll = ['FR_fyear', 'FR_tyear', 'FR_twoyear', 'FR_year', 'FR_nowyear', 'FR_hyear', 'FR_tmonth', 'FR_month',
        #          'FR_week', 'code', 'name', 'asset', 'clrq', 'levelOfRisk', 'manager', 'maxStar', 'net', 'totalnet1',
        #          'orgname', 'week', 'month', 'tmonth', 'hyear', 'year', 'tyear', 'JJType', 'fyearZF', 'startZF', 'HC',
        #          'XP', 'BD', 'manageHBL', 'startManage', 'manageDay', 'workDay', 'yearHBL', 'JLlevel', 'GPstock',
        #          'Source', 'date', 'preprice', 'price', 'priceRate', 'rate', 'S_JL', 'S_zq', 'S_zd', 'S_zs', 'stand_1',
        #          'stand_2', 'STABLE_1', 'STABLE_2', 'EXCITED_1', 'EXCITED_2']

        return compOut

        # print(0)


if __name__ == "__main__":
    FM = Fund_manager()
    FM.SCORE('zj_codes')
    # print(FM.getRZDF('163406'))
