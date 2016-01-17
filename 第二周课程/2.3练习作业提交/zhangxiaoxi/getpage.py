# -*- coding:utf-8 -*-
import pymongo
import requests
import re
import time
from bs4 import BeautifulSoup
client =pymongo.MongoClient('localhost',27017)
walden=client['ganjiwang']
url_list=walden['url_list']
def getPage():
    pages=0
    judge=1
    while judge!=0:
        list_view='http://bj.58.com/shoujihao/pn{}/'.format(str(pages))
        wb_data=requests.get(list_view)
        time.sleep(1)
        soup = BeautifulSoup(wb_data.text,'lxml')
        items=soup.select('#infolist > div > ul > div.boxlist > ul > li > a.t')
        judge=len(items)
        pages=pages+1
        for link in items:
            item_link=link.get('href').split('?')[0]
            pattern = re.compile(r'\w+')
            content = re.findall(pattern,item_link)
            m=re.match('shoujihao', content[4])
            if m:
                url_list.insert_one({'url':item_link})
                print item_link
    print pages
