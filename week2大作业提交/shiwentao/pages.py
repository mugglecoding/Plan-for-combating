#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'stone'

from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017,connect=False)
ganji = client['test']
url_list = ganji['url_list']
item_info = ganji['item_info']

# 2个爬虫
#第一个获取每个分类下的所有链接
#第二个爬虫,获取每个链接中的信息

#urls = []


def get_links_from_channel(channel,pages,who_sells=3):
    list_view = '{0}a{1}0{2}/'.format(channel,str(who_sells),str(pages))
    wb_data = requests.get(list_view)
    time.sleep(1)
    soup = BeautifulSoup(wb_data.text,'lxml')
    # 手机号码页面
    if channel.__eq__('http://bj.ganji.com/shoujihaoma/') and pages>34:
        pass
    if soup.find('div','phone-list'):
        for link in soup.select('a.pn-lbox'):
            item_link = link.get('href')
            url_list.insert_one({'url':item_link,'visited':0})
            #print item_link
    else:
        pass
    # 通用页面
    if soup.find('li','js-item'):
        for link in soup.select('ul li.js-item'):
            item_link = '{0}{1}x.htm'.format(channel,link.get('data-puid'))
            url_list.insert_one({'url':item_link,'visited':0})
            #print item_link
    else:
        pass


def get_info_from_url(url):
    wb_data = requests.get(url)
    time.sleep(1)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    if soup.find('div', 'error'):
        pass
    else:
        title = soup.title.text
        price = soup.select('i.f22')[0].text
        fenlei = list(soup.select('ul.det-infor li:nth-of-type(1) span')[0].stripped_strings)
        area = list(soup.select('ul.det-infor li:nth-of-type(3)')[0].stripped_strings)
        area.pop(0) if area.__len__()>0 else None
        date = soup.select('ul.title-info-l li i.pr-5')[0].text if soup.select('ul.title-info-l li i.pr-5')[0].text.strip().__len__()>0 else None
        item_info.insert_one({'title':title,'price':price,'type':fenlei,'area':area,'time':date})
        #print {'title':title,'price':price,'type':type,'area':area,'time':time}

#get_links_from_channel('http://bj.ganji.com/shoujihaoma/',10)
#get_info_from_url('http://bj.ganji.com/taishidiannaozhengji/1070383590x.htm')
