# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/47.0.2526.106 Chrome/47.0.2526.106 Safari/537.36'
headers = { 'User-Agent' : user_agent }
def getFenlei():
    list_view='http://bj.ganji.com/wu/'
    wb_data=requests.get(list_view,headers = headers)
    soup = BeautifulSoup(wb_data.text,'lxml')
    items=soup.select('div.content > div.clearfix > div > dl.fenlei > dt > a')
    fenlei=[]
    for link in items:
        fenlei.append(link.get('href'))
    return fenlei

