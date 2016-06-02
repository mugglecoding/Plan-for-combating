#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pymongo
import requests
from bs4 import BeautifulSoup

# 连接MongoDB，数据库地址为:localhost。端口号为: 27017
client = pymongo.MongoClient('localhost', 27017)

# 从MongoDB中选择名称为 xiaozhu 的数据库
xiaozhu = client['xiaozhu']

# 从 xiaozhu 数据库选择名称为 fangzi 的表
fangzi = xiaozhu['fangzi']


def insert_fangzi_info(url):
    # 请求列表页面，获取页面数据
    wb_data = requests.get(url)

    # 开始解析数据，采用lxml解析引擎
    soup = BeautifulSoup(wb_data.text, 'lxml')

    # Chrome浏览器打开网页，把鼠标放到标题和价格信息上，右键，审查元素（检查元素），Copy Css Path，去掉:nth-child()
    titles = soup.select('span.result_title')
    prices = soup.select('span.result_price > i')

    # 通过for取出列表中的标签，然后通过get_text()获取标签内的文本
    for title, price in zip(titles, prices):
        # price.get_text() 得到的是字符串，需要int()函数转成数字类型
        info = {
            'title': title.get_text(),
            'price': int(price.get_text())
        }
        fangzi.insert_one(info)


def find_fangzi():
    # 从xiaozhu数据库的fangzi表，查询所有数据，用find()函数
    for info in fangzi.find():
        # info 我们插入的数据都有title和price，我们取出每条信息的price，用来比较
        if info['price'] >= 500:
            print(info)

# 根据规律，生成3个列表页面链接
urls = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(number) for number in range(1, 4)]

# 从链接列表中，用for一个个取出来
for single_url in urls:
    # 把得到的列表页面链接，传给函数，这个函数提取房子的标题和价格
    insert_fangzi_info(single_url)
