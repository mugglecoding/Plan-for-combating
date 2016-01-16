# __author__ = 'xjlin'
# -*- coding: utf-8 -*-

import requests
import time
import re
from bs4 import BeautifulSoup

headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
}


url = 'http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'

wb_data = requests.get(url)

soup = BeautifulSoup(wb_data.text, 'lxml')

hrefs = soup.select('td.t > a')

#detail_url = 'http://bj.58.com/pingbandiannao/24517179000509x.shtml?psid=170801987190281724635921968&entinfo=24517179000509_0&iuType=p_0&PGTID=0d305a36-0000-1d8b-4afe-dd3a99ef2c8f&ClickID=5'

prefix_js = 'http://jst1.58.com/counter?infoid='



def get_id(url):
    info = re.findall(r'[\d]+', url)
    return(info[-2])


def get_rev(prefix_url, suffix_url):
    str = prefix_url + suffix_url
    jsdata = requests.get(str)
    soup_js = BeautifulSoup(jsdata.text, 'lxml')
    res = soup_js.select('p')
    for rr in res:
        a = re.findall(r'[\d|.]+', rr.get_text())
        result = a[4]
    return result


def get_info(url, data = None):
    time.sleep(2)
    detail_data = requests.get(url, headers = headers)
    soup_detail = BeautifulSoup(detail_data.text, 'lxml')
    titles = soup_detail.select('div.col_sub.mainTitle > h1')
    times = soup_detail.select('ul.mtit_con_left.fl > li.time')

    prices = soup_detail.select('div.su_con > span.price.c_f50')
    types = soup_detail.select('p.c_666 > span')
    areas = soup_detail.select('#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li:nth-of-type(3) > div.su_con > span > a:nth-of-type(1)')
    categories = soup_detail.select('#header > div.breadCrumb.f12 > span:nth-of-type(3) > a')
    #print(titles, reviews, times, prices, types, areas, categories)
    #print(categories)
    #time.sleep(2)
    if areas == []:
        for title, tim, price, type, category in zip(titles, times, prices, types, categories):
            if(type.get_text() == '\n'):
                data = {
                    'title' : title.get_text(),
                    'time'  : tim.get_text(),
                    'review': get_rev(prefix_js, get_id(url)),
                    'price' : price.get_text(),
                    'type'  : '个人',
                    'area'  : '未指定区域',
                    'category' : list(category.stripped_strings)
                }
                print(data)
            else:
                data = {
                    'title' : title.get_text(),
                    'time'  : tim.get_text(),
                    'review': get_rev(prefix_js, get_id(url)),
                    'price' : price.get_text(),
                    'type'  : '商家',
                    'area'  : '未指定区域',
                    'category' : list(category.stripped_strings)
                }
                print(data)
    else:
        for title, tim, price, type, area, category in zip(titles, times, prices, types, areas, categories):
            if(type.get_text() == '\n'):
                data = {
                    'title' : title.get_text(),
                    'time'  : tim.get_text(),
                    'review': get_rev(prefix_js, get_id(url)),
                    'price' : price.get_text(),
                    'type'  : '个人',
                    'area'  : area.get_text(),
                    'category' : list(category.stripped_strings)
                }
                print(data)
            else:
                data = {
                    'title' : title.get_text(),
                    'time'  : tim.get_text(),
                    'review': get_rev(prefix_js, get_id(url)),
                    'price' : price.get_text(),
                    'type'  : '商家',
                    'area'  : area.get_text(),
                    'category' : list(category.stripped_strings)
                }
                print(data)


for href in hrefs:
    get_info(href.get('href'))
    #print(href.get('href'))


