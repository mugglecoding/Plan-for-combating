# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

start_url = 'http://bj.ganji.com/wu/'
host_url = 'http://bj.ganji.com'

def get_channel_urls(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text,'lxml')
    links = soup.select('dl.fenlei dt a')
    for link in links:
        page_url = host_url + link.get('href')
        print page_url

get_channel_urls(start_url)

channel_list = '''
    http://bj.ganji.com/jiaju/
    http://bj.ganji.com/rirongbaihuo/
    http://bj.ganji.com/shouji/
    http://bj.ganji.com/shoujihaoma/
    http://bj.ganji.com/bangong/
    http://bj.ganji.com/nongyongpin/
    http://bj.ganji.com/jiadian/
    http://bj.ganji.com/ershoubijibendiannao/
    http://bj.ganji.com/ruanjiantushu/
    http://bj.ganji.com/yingyouyunfu/
    http://bj.ganji.com/diannao/
    http://bj.ganji.com/xianzhilipin/
    http://bj.ganji.com/fushixiaobaxuemao/
    http://bj.ganji.com/meironghuazhuang/
    http://bj.ganji.com/shuma/
    http://bj.ganji.com/laonianyongpin/
    http://bj.ganji.com/xuniwupin/
    http://bj.ganji.com/qitawupin/
    http://bj.ganji.com/ershoufree/
    http://bj.ganji.com/wupinjiaohuan/
'''

