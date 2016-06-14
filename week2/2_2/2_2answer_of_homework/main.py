#!/usr/bin/env python
#-*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup
import pymongo

# 连接MongoDB，数据库地址为:localhost。端口号为: 27017
# 注意MoongoClient大小写，不要写成mongoclient
client = pymongo.MongoClient('localhost', 27017)

# 从MongoDB中选择名称为 tongcheng 的数据库
tongcheng = client['tongcheng']

# 从 xiaozhu 数据库选择名称为 shoujihao 的表
shoujihao = tongcheng['shoujihao']


def get_shoujihao():
    for number in range(1, 10000):
        url = 'http://bj.58.com/shoujihao/pn{}/'.format(number)

        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.text, 'lxml')

        numbers = soup.select('strong.number')
        prices = soup.select('b.price')
        links = soup.select('a.t')
        totals = soup.select('#infocont > span > b')

        for number, price, link, total in zip(numbers, prices, links, totals):
            total_value = int(total.get_text())
            if total_value == 0:
                return

            data = {
                'title': number.get_text(),
                'price': price.get_text(),
                'link': link.get('href')
            }
            shoujihao.insert_one(data)
            print(data)
    print('Done')


get_shoujihao()
