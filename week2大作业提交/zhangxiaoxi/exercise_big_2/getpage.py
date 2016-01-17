# -*- coding:utf-8 -*-
import pymongo
import requests
import re
import time
from multiprocessing import Pool
from getfenlei import getFenlei
from bs4 import BeautifulSoup
client =pymongo.MongoClient('localhost',27017)
walden=client['ganjiwang']
url_list=walden['url_list']
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/47.0.2526.106 Chrome/47.0.2526.106 Safari/537.36'
headers = { 'User-Agent' : user_agent }
def getPage(fenlei):
    pages=1
    judge=1
    while judge!=0:
        list_view='http://bj.ganji.com{}o{}/'.format(fenlei,str(pages))
        wb_data=requests.get(list_view,headers=headers)
        time.sleep(1)
        soup = BeautifulSoup(wb_data.text,'lxml')
        items=soup.select('dd.feature > div > ul > li > a')
        pageLink=soup.select('.pageLink')
        judge=len(pageLink)
        pages=pages+1
        for link in items:
            item_link=link.get('href')
            print(item_link)
            pattern = re.compile(r'\w+')
            content = re.findall(pattern,item_link)
            m=re.match(fenlei, content[4])
            if m:
                url_list.insert_one({'url':item_link})
                print item_link
def get_page_from_fenlei():
    fenleis=getFenlei()
    pool=Pool()
    pool.map(getPage,fenleis)
get_page_from_fenlei()


'''
li.js-item
#wrapper > div.leftBox > div.layoutlist > dl:nth-child(2) > dd.feature > div > ul > li > a
'''