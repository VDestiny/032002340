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
       '内蒙古', '广西', '西藏', '宁夏', '新疆', '香港', '澳门'
]

headers =  {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27',
        'Referer' : 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml',
        'Cookie': 'yfx_c_g_u_id_10006654=_ck22091015454118598777723981237; sVoELocvxVW0S=5DSg3AJl0Eh2sJMRS0xBrJW.qk641GDuqy0w_08ci5Ki5RdtDaxR5X6SCxJU2lUT2JAIRrk5bgMicvJNmcncBLA; insert_cookie=91349450; _gscu_2059686908=62796040qrs9mc90; _gscbrs_2059686908=1; yfx_f_l_v_t_10006654=f_t_1662795941823__r_t_1662866266927__v_t_1662876292876__r_c_1; security_session_verify=ce983d3c2eeacced2208f3cd4fc9e426; sVoELocvxVW0T=53STdBCWwGhlqqqDkt0rQtG6hvNNyjExrIU3bZflvEnBgUiy0rpSXvPhIFquw.HpHkcLWwzYGQ6eEHopJXmPiqMH7P7nL09.CikMkdGvjHqdEVKzpKiFU60R530mcGomp82jqaQL3a.guQHYmHnb8EGk9nyNGpDJtpIqUlaBaWa4wQtfM3rt96HTunysuql4i5fPS4RFVke8_drqEBZUr9U8w4Ft1xHFp8bgYNqx9XEZOpYCBVMHCFEDNKT2fB88YtHP1XwYLY6rySFRX0sxoeyl3y8i5WhmKypGqBUkoSGuy.tTEACdvFM9IJQglti.iCaRYfu4_EvP28kJ69CTWulvhNH1OSwC6nG1zr6BzkvTG'
}

urll = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd{}.shtml'
urlll = 'http://www.nhc.gov.cn'

def calculate_one (page):
    #根据页码计算出一级url
    if page==1:     
        url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml'
    else:
        url = urll.format('_'+str(page))
    #利用一级url进入界面获取二级url
    return url

def calculate_two (url):          
    #获取二级页面url
    response = requests.get(url=url, headers=headers)
    #将一级界面数据内容存入page_text
    page_text = response.text
    #在一级中依次进入24个二级页面
    for i in range(0, 24):
        soup = BeautifulSoup(page_text, 'lxml')
        s = soup.select('.list> ul a')[i]['href']
        url = urlll + s
        print(url)
        #算出url后爬取数据
        acquire_data(url)     

def acquire_data(url):      
    #爬取数据
    response = requests.get(url=url, headers=headers)
    page_text = response.text
    #将二级界面数据内容进行处理
    soup = BeautifulSoup(page_text, 'lxml')
    s = soup.select('.con > p')
    a = ''
    for i in s:
        b = ''.join(i.text)
        a = a + b       #a中存有页面数据
    date = str(get_date(page_text))
    sure = str(get_day_all_data_sure(a))
    unsure = str(get_day_all_data_unsure(a))
    get_day_provincedata(a)
    get_day_HKAMTW(a)
    #写入excel
    write_excel(date, sure, unsure)

def get_date(page_text):
    #获取日期
    soup = BeautifulSoup(page_text, 'lxml')
    s = soup.select('title')
    pattern = re.compile(r'\d+月\d+日')
    z = pattern.findall(str(s))
    date = "".join(z)
    print(date)
    return (date)

def get_day_all_data_sure(a):
    #获取本土当日疫情情况         
        #获取本土新增确诊
    pattern = re.compile('新疆生产建设兵团报告新增确诊病例\d+例')
    result = pattern.findall(str(a))
    pattern = re.compile('\d+')
    z = pattern.findall(str(result))
    sure = "".join(z)
    print(sure)
    return (sure)

def get_day_all_data_unsure(a):
    #获取本土当日疫情情况  
        #获取本土无症状新增确诊
    pattern = re.compile('新疆生产建设兵团报告新增无症状感染者\d+例')
    result = pattern.findall(a)
    pattern = re.compile('\d+')
    z = pattern.findall(str(result))
    unsure = "".join(z)
    print(unsure)
    return (unsure)

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

def write_excel(date, sure, unsure):
    xfile = vv.load_workbook('COVID2.xlsx')
    ws = xfile.get_sheet_by_name('Sheet')
    ws.append([str(date), str(sure), str(unsure)]+ L)
    xfile.save('COVID2.xlsx')

def make_excel():
    xfile = vv.Workbook() # 创建工作簿对象
    ws = xfile['Sheet'] # 创建子表
    ws.append(['日期/省份', '本土新增', '本土无症状']+ Province)
    xfile.save('COVID2.xlsx')

if __name__ == '__main__':
    #创建excel
    make_excel()
    # write_excel('9月2日', 2, 3)

    #从42页数据中获取二级url的尾部数据
    for i in range(1, 2):
        #计算一级页面url
        url = calculate_one(i)     
        
        #获取二级页面url
        url = calculate_two(url)

    