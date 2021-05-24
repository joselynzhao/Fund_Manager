#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/5/23 下午9:43
# @Author  : Joselynzhao
# @Email   : zhaojing17@forxmail.com
# @File    : Codes_infor.py
# @Software: PyCharm
# @Desc    :


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

care_list_zj = {
    'name': 'zj_持有',
    'codes': ['100020',
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
              '163406',

              ]}
guanwang_zj ={
    'name':'zj_关注',
    'codes':[
        '003860',
        '675113',
        '217022',
        '160632',
        '161122',
        '501009',
        '161726',
        '000248',
        '006733',
        '006102',
        '005876',
        '004131',
        '007994',
        '502000',
        '160420',
        '007464',
        '180003',
        '004788',
        '005875','169104',
        '003940',
        '001102',
        '001679',
        '003984',
        '519150',
        '000209',
        '001951',
        '161005'
    ]
}

temp_list={
    'name':'测试',
    'codes':[
        '519729',
        ''
    ]
}

care_list_dd1 = {
    'name': 'dd1_持有',
    'codes': [
        '003860',
        '675113',
        '377240',
        '217022',
        '008888',
        '001630',
        '005224',
        '003634',
        '003547',
        '009098',
        '161716',
        '011854',
        '008714',
        '005609',
        '121012',
        '009548',
        '011206',
        # '968010',
        '008903',
        '202003',
        '519066',
        '160212',
        '002379',
        '160211']
}
care_list_dd2 = {
    'name': 'dd2_持有',
    'codes': [
        '161725',
        '160222',
        '003095',
        '000409',
        # '010378',
        '001508',
        '110022',
        '001076',
        '000083',
        '001975',
        '519772',
        '005911',
        '007412',
        '001606',
        '001645',
        '000309',
        '002259',
        '206007',
        '005827',
        # '010681',
        '270002',
        '002851',
        '690007',
        # '011223',
        '160716',
        '000988',
        '163415',
        '519732',
        '164906',
        '001179',
        '450001',
        '163402']
}
