# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import pymongo

client = pymongo.MongoClient('localhost',27017)
week2 = client['week2']
url_list = week2['url_list']
item_info  = week2['iteminfo']

def get_links_from(channel,pages,who_sells='o'):
    #http://bj.ganji.com/jiaju/o2/
    list_view = '{}{}{}/'.format(channel,who_sells,str(pages))
    request = requests.get(list_view)
    soup = BeautifulSoup(request.text,'lxml')
    time.sleep(2)
    if len(soup.select('a.ft-tit')):
        for link in soup.select('a.ft-tit'):
            item_link = link.get('href')
            url_list.insert_one({'url' : item_link})
            print item_link
    else:
        pass

def get_item_info(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text,'lxml')
    error = soup.select('p.error-tips1')

    if error:
        pass
    else:
        title = soup.select('h1.title-name')[0].text
        date = soup.select('i.pr-5')[0].text
        type = soup.select(' ul.det-infor  li  span  a')[0].text
        price = soup.select(' i.f22.fc-orange.f-type')[0].text
        #area =soup.select('ul.det-infor li a')[2:]
        item_info.insert_one({'title':title,'date':date,'type':type,'price':price})

        print {'title':title,'date':date,'type':type,'price':price}
