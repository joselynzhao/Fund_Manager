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

# http://fund.eastmoney.com/005296.html
# url1 = 'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&secids=1.000001,0.399001&invt=2&fields=f2,f3,f4,f6,f12,f104,f105,f106&ut=267f9ad526dbe6b0262ab19316f5a25b&cb=jQuery18307458225946461923_1621588092653&_=1621588092705'
'''
0 上证指数　ｆ104涨　
'''

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


class Fund_manager():
    def __init__(self):
        self.care_list_zj = ['100020',
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
        self.headers = {'User-Agent': random.choice(user_agent_list), 'Referer': referer_list[0]}  # 每次运行的时候都会重新生成头部

    def getUrl(self, fscode):  # 同花顺查询单只基金固定信息
        try:
            return 'http://fund.10jqka.com.cn/data/client/myfund/' + fscode
        except Exception as e:
            print(e)
            code = str(fscode)  # 转换为ｓｔｒ格式
            return 'http://fund.10jqka.com.cn/data/client/myfund/' + code

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
        print("正在爬取第二部分数据……")
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

    def updata_Cares_VIP(self, query_list, file_name, sheet_name):
        infor1 = {}
        print("正在爬取第一部分数据……")
        for i in tqdm(range(len(query_list))):
            code = query_list[i]
            data1 = self.getWorth_infor1(code)
            infor1[code] = data1
        infor2 = self.getWorth_Valuation_forList(query_list)
        print("正在爬取第三部分数据……")
        infor3 = {}
        for i in tqdm(range(len(query_list))):
            code = query_list[i]
            data3 = self.getInfo_fromApp(code)
            infor3[code] = data3
        df1 = pd.DataFrame(infor1)
        df2 = pd.DataFrame(infor2)
        df3 = pd.DataFrame(infor3)
        df1 = df1.transpose()
        df2 = df2.transpose()
        df3 = df3.transpose()

        df2 = df2[['code', 'date', 'preprice', 'price', 'priceRate', 'rate']]
        df2[['code']] = df2[['code']].astype(str)
        df1 = df1[['code', 'name', 'asset', 'clrq', 'levelOfRisk', 'manager', 'maxStar', 'net', 'orgname',
                   'sgstat',
                   'shstat', 'week', 'month', 'tmonth', 'hyear', 'year', 'tyear']]  # 取出我要用的数据
        df1[['code']] = df1[['code']].astype(str)
        # df3都是中文字段　并且没有code
        # 先合并１２
        results = pd.concat([df1, df2], axis=1, join='outer')
        results = results[
            ['code', 'name', 'asset', 'clrq', 'levelOfRisk', 'manager', 'maxStar', 'orgname', 'sgstat',
             'shstat', 'date', 'preprice', 'price', 'priceRate', 'net', 'rate', 'week', 'month', 'tmonth', 'hyear',
             'year', 'tyear']]
        # print(df3.columns.to_list())
        results.columns = ['编码１', '编码２', '名称', '规模(亿)', '成立时间', '风险等级', '基金经理', '基金评级', '基金公司', '申购状态',
                           '赎回状态', '当前日期', '基金净值', '当日估值', '估值增长(%)', '当日单位净值', '日增长率-收盘(%)', '近1周涨幅(%)', '近1月涨幅(%)',
                           '近3月涨幅(%)', '近6月涨幅(%)', '近1年涨幅(%)', '近3年涨幅(%)']

        results_Vip = pd.concat([results, df3], axis=1, join='outer')
        # 调整columns顺序
        results_Vip = results_Vip[
            ['编码１', '编码２', '名称', '基金类型', '风险等级', '股票重仓', '基金经理', '任期起点', '基金公司', '规模(亿)', '成立时间', '任职回报率(%)', '任期时长',
             '从业时长', '年均回报率(%)', '基金经理等级', '基金评级', '近3年涨幅(%)', '近5年涨幅(%)', '成立以来涨幅(%)', '近１年最大回撤(%)', '近１年夏普比率',
             '近１年波动率(%)', '近1周涨幅(%)', '近1月涨幅(%)',
             '近3月涨幅(%)', '近6月涨幅(%)', '近1年涨幅(%)', '申购状态', '赎回状态', '当前日期', '基金净值', '当日估值', '估值增长(%)', '当日单位净值',
             '日增长率-收盘(%)']]
        # 转换数据类型
        # df3[['成立时间','当前日期']] = df3[['成立时间','当前日期']].apply(pd.to_datetime)
        try:
            results_Vip[
                ['规模(亿)', '基金净值', '当日估值', '估值增长(%)', '当日单位净值', '日增长率-收盘(%)', '近1周涨幅(%)', '近1月涨幅(%)', '近3月涨幅(%)',
                 '近6月涨幅(%)', '任职回报率(%)', '年均回报率(%)',
                 '近1年涨幅(%)', '近3年涨幅(%)', '近5年涨幅(%)', '成立以来涨幅(%)', '近１年最大回撤(%)', '近１年夏普比率', '近１年波动率(%)']].apply(
                pd.to_numeric)
        except Exception as e:
            print(e)

        # 　下面尝试这计算基金评分
        # self.comp_Score(results_Vip[['规模(亿)', '成立时间', '任职回报率(%)', '任期时长',
        #      '从业时长', '年均回报率(%)', '基金经理等级', '基金评级', '近3年涨幅(%)', '近5年涨幅(%)', '成立以来涨幅(%)', '近１年最大回撤(%)', '近１年夏普比率',
        #      '近１年波动率(%)']])

        # 写入数据到文件

        try:
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(t)
            results_Vip.to_excel(f'OUTPUTS/{file_name}_{t}.xlsx', f'{sheet_name}', index=None, encoding='utf-8')
        except Exception as e:
            print(e)
        print(0)

    def comp_Score(self):
        datas  = pd.read_excel("./基金关注_2021-05-22 11:03:06.xlsx")
        v_datas = datas[['编码２','规模(亿)', '成立时间', '任职回报率(%)', '任期时长',
             '从业时长', '年均回报率(%)', '基金经理等级', '基金评级', '近3年涨幅(%)', '近5年涨幅(%)', '成立以来涨幅(%)', '近１年最大回撤(%)', '近１年夏普比率',
             '近１年波动率(%)']]
        print(v_datas)



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
        All_INFO['股票重仓'] = JJCC['InverstPosition']['fundStocks'][0]['GPJC'] + ',' + \
                           JJCC['InverstPosition']['fundStocks'][1]['GPJC'] + ',' + \
                           JJCC['InverstPosition']['fundStocks'][2]['GPJC']
        # df = pd.DataFrame(All_INFO)
        # print(0)
        return All_INFO


if __name__ == "__main__":
    FM = Fund_manager()
    FM.updata_Cares_VIP(FM.care_list_zj, '基金关注', 'zhaojing_care')
    # FM.comp_Score()
