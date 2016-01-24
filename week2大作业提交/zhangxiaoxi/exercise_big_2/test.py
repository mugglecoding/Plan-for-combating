# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
def getPage():
    list_view='http://bj.ganji.com/wu/'
    wb_data=requests.get(list_view)
    soup = BeautifulSoup(wb_data.text,'lxml')
    items=soup.select('div.content > div.clearfix > div > dl.fenlei > dt > a')
    for link in items:
        item_link=link.get('href')
        print(item_link)
getPage()