#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import random
import pymongo
import requests
from bs4 import BeautifulSoup

# 注意不要写错localhost
client = pymongo.MongoClient('localhost', 27017)
# 注意不要把中括号写成了小括号
ganji = client['ganji']
url_list = ganji['url_list']
item_info = ganji['item_info']

headers  = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Connection':'keep-alive'
}

# http://cn-proxy.com/
proxy_list = [
    'http://117.177.250.151:8081',
    'http://111.85.219.250:3129',
    'http://122.70.183.138:8118',
    ]
# 随机获取代理ip
proxy_ip = random.choice(proxy_list) 
proxies = {'http': proxy_ip}

# 获取所有的列表页面链接
def get_links_from(channel, page, who_sell='o'):
    # http://bj.ganji.com/ershoubijibendiannao/o3/
    # o for personal a for merchant
    url = '{}{}{}/'.format(channel, who_sell, page)
    wb_data = requests.get(url, headers=headers, proxies=proxies)
    # 检查页面是否不存在，或者被封ip
    if wb_data.status_code == 200:
        soup = BeautifulSoup(wb_data.text, 'lxml')
        for link in soup.select('.fenlei dt a'):
            item_link = link.get('href')
            url_list.insert_one({'url': item_link})
            get_item_info_from(item_link)
            print(item_link)

# 获取指定链接页面详细信息
def get_item_info_from(url, data=None):
    wb_data = requests.get(url, headers=headers)
    # 检查页面是否不存在，或者被封ip
    if wb_data.status_code != 200:
        return
    
    soup = BeautifulSoup(wb_data.text, 'lxml')
    
    prices = soup.select('.f22.fc-orange.f-type')
    pub_dates = soup.select('.pr-5')
    areas = soup.select('ul.det-infor > li:nth-of-type(3) > a')
    cates = soup.select('ul.det-infor > li:nth-of-type(1) > span')
    
    data = {
        'title': soup.title.text.strip(),
        'price': prices[0].text.strip() if len(prices) > 0 else 0,
        'pub_date': pub_dates[0].text.strip().split(' ')[0] if len(pub_dates) > 0 else "",
        'area': [area.text.strip() for area in areas if area.text.strip() != "-"],
        'cates': [cate.text.strip() for cate in cates],
        'url':url
    }
    print(data)
    item_info.insert_one(data)
