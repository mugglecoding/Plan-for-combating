#!/usr/bin/env python
#-*- coding:utf-8 -*-
_author__ = 'stone'

from bs4 import BeautifulSoup
import requests

url = 'http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'
html = requests.get(url)

info = []

#分离方法
def find(table):
    for item in table:
        if item.select('tr') is not None:
            a = item.select('tr > td.t > a.t')
            # 地区时间卖家　在同一个span里　
            area_time_seller = item.select('tr > td.t > span.fl')
            price = item.select('tr > td.tc > b.pri')
            for a,area_time_seller, price in zip(a,area_time_seller,price):
                if area_time_seller.get_text().split('/').__len__() == 3:
                    area = area_time_seller.get_text().split('/')[0]
                    time = area_time_seller.get_text().split('/')[1]
                    seller = area_time_seller.get_text().split('/')[2]
                else :
                    area = area_time_seller.get_text().split('/')[0]
                    time = area_time_seller.get_text().split('/')[1]
                    seller = '个人'
                # 浏览数需要具体信息里查找
                href = a.get('href')
                html_a = requests.get(href)
                s = BeautifulSoup(html_a.text,'lxml')
                review = s.select('#totalcount')[0]
                #print a.get_text(),time,price.get_text(),seller,area,review.get_text()
                #print '-------------------------------------------------'
                datas = {
                    '标题':a.get_text(),
                    '时间':time,
                    '价格':price.get_text(),
                   '卖家类型':seller,
                    '地区':area,
                    '浏览量':review.get_text()
                }
                info.append(datas)

soup = BeautifulSoup(html.text,'lxml')
# 非顶部table
table = soup.select(' #infolist > table ')
# 顶部table
table_top = soup.select('#infolist > div.pr > table')
# 分类
type = soup.select('#infolist > div > table > tr > td > div > h1')

find(table_top)
find(table)



