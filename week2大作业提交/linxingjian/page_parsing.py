# __author__ = 'xjlin'
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
url_list = ganji['url_list']
item_info = ganji['item_info']

#爬取一般页面的所有链接
#若爬取手机页面,则可以将页面内的都爬出来,若爬取其他页面,则会爬出页面内搜索不到的内容,原因目前未知,暂存疑
def get_link_from(channel, pages, who_sells = 'a1'):
    list_view = '{}{}o{}/'.format(channel, str(who_sells), str(pages))
    type = channel.split('/')
    wb_data = requests.get(list_view)
    time.sleep(2)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    if soup.find('div','pageBox'):
        for link in soup.select('div.ft-db > ul > li'):
            item_link = 'http://bj.ganji.com/' + type[-2]+ '/' + link.get('data-puid') + 'x.htm'
            url_list.insert_one({'url' : item_link})

    else:
        pass
#get_link_from('http://bj.ganji.com/ershoubijibendiannao/', 1)

#爬取手机号页面的所有链接
def get_plink_from(channel, pages, who_sells = 'a1'):
    list_view = '{}{}o{}/'.format(channel, str(who_sells), str(pages))
    wb_data = requests.get(list_view)
    time.sleep(2)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    if soup.find('a','next'):
        for link in soup.select('div.phone-list.clearfix > div.pn-list > a'):
            item_link = link.get('href')
            url_list.insert_one({'url' : item_link})
    else:
        pass

#get_plink_from('http://bj.ganji.com/shoujihaoma/', 2)



#爬取一般商品的详情
def get_item_info(url):
    wb_data = requests.get(url)
    time.sleep(2)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    no_longer_exist = soup.select('div.error')
    if no_longer_exist:
        pass
    else:
        title = list(soup.select('h1.title-name'))[0].get_text()
        price = soup.select('i.f22.fc-orange.f-type')[0].get_text()
        data = soup.select('i.pr-5')[0].get_text()
        if data == '\n':
            data = 'no data'
        else:
            data = soup.select('i.pr-5')[0].get_text().split()[0]
        #data = soup.select('i.pr-5')[0].get_text().split()[0]
        stype = soup.select('span.fc-orange')[0].get_text()
        if stype == '':
            stype = '个人'
        else:
            stype = '商家'
        itype = soup.select('ul.det-infor > li:nth-of-type(1) > span > a')[0].get_text()
        area = list(soup.select('ul.det-infor > li:nth-of-type(3)')[0].stripped_strings)
        area = area[1:10]
        item_info.insert_one({'title': title, 'price': price, 'data' : data, 'area' : area, 'item-type': itype, 'sell-type':stype})
        #print({'title': title, 'price': price, 'data' : data, 'area' : area, 'type': itype })


#get_item_info('http://bj.ganji.com/jiadian/1723899084x.htm')

# #爬取手机的详情
# def get_phone_info(url):
#     wb_data = requests.get(url)
#     time.sleep(2)
#     soup = BeautifulSoup(wb_data.text, 'lxml')
#     no_longer_exist = soup.select('div.error')
#     if no_longer_exist:
#         pass
#     else:
#         title = list(soup.select('h1.title-name'))[0].get_text()
#         price = soup.select('i.f22.fc-orange.f-type')[0].get_text()
#         stype = soup.select('span.fc-orange')[0].get_text()
#         if stype == '':
#             stype = '个人'
#         else:
#             stype = '商家'
#         itype = soup.select('ul.det-infor > li:nth-of-type(1) > span > a')[0].get_text()
#         area = list(soup.select('ul.det-infor > li:nth-of-type(3)')[0].stripped_strings)
#         area = area[1:10]
#         item_info.insert_one({'title': title, 'price': price, 'data' : 'no data', 'area' : area, 'item-type': itype, 'sell-type':stype})


#爬取手机号的详情
def get_pnumber_info(url):
    wb_data = requests.get(url)
    time.sleep(2)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    no_longer_exist = soup.select('div.error')
    if no_longer_exist:
        pass
    else:
        title = list(soup.select('h1.title-name'))[0].get_text()
        price = soup.select('b.f22.fc-orange.f-type')[0].get_text()
        stype = soup.select('span.fc-orange')[0].get_text()
        if stype == '':
            stype = '个人'
        else:
            stype = '商家'
        itype = soup.select('ul.det-infor > li:nth-of-type(1) > span > a')[0].get_text()
        area = list(soup.select('ul.det-infor > li:nth-of-type(2)')[0].stripped_strings)
        area = area[1:10]
        item_info.insert_one({'title': title, 'price': price, 'data' : 'no data', 'area' : area, 'item-type': itype, 'sell-type':stype})



