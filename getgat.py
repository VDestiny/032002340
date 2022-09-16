from argparse import ONE_OR_MORE
from datetime import datetime
from pkgutil import get_data
from sqlite3 import Date
from ssl import DER_cert_to_PEM_cert
import string
from telnetlib import SUPPRESS_LOCAL_ECHO
from bs4 import BeautifulSoup
import openpyxl as vv
import requests
import re

L = [0] * 34
Province = [
    '北京', '天津', '上海', '重庆', '河北', '山西', '辽宁', '吉林', '黑龙江',
     '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南',
      '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '台湾',
       '内蒙古', '广西', '西藏', '宁夏', '新疆', '香港', '澳门',
]

def get_day_provincedata(a):
    #获取各省份当日疫情情况
        #获取各省份新增确诊
    pattern = re.compile('本土病例\d+例（.*?），含')
    result = pattern.findall(a)
    for i in range(0,34):
        pattern = re.compile (r'{}\d+'.format(Province[i]))
        result2 = pattern.findall(str(result))
        pattern = re.compile("\d+")
        z = pattern.findall(str(result2)) 
        L[i] = "".join(z)
        
        print(Province[i], L[i])

def get_day_HKAMTW(a):
    #获取香港当日疫情情况
    pattern = re.compile('香港特别行政区\d+例')
    result = pattern.findall(a)
    pattern = re.compile("\d+")
    z = pattern.findall(str(result)) 
    L[26] = "".join(z)

    #获取澳门当日疫情情况
    pattern = re.compile('澳门特别行政区\d+例')
    result = pattern.findall(a)
    pattern = re.compile("\d+")
    z = pattern.findall(str(result)) 
    L[33] = "".join(z)

    #获取台湾当日疫情情况
    pattern = re.compile('台湾地区\d+例')
    result = pattern.findall(a)
    pattern = re.compile("\d+")
    z = pattern.findall(str(result)) 
    L[32] = "".join(z)
