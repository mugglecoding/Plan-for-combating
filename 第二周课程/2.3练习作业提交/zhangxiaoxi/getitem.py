# -*- coding:utf-8 -*-
import urllib2
import pymongo
import re
from bs4 import BeautifulSoup
from multiprocessing import Pool
client =pymongo.MongoClient('localhost',27017)
walden=client['58shoujihao']
url_list=walden['url_list']
content_list=walden['content_list']
def getPageItems():
    for href in content_list.find({}, {'url' : 1}):
       if href in url_list.find({}, {'url' : 1}):
           print  '已抓取过'
       else:
        url=href.get('url')
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        pageCode = response.read().decode('utf-8')
        soup = BeautifulSoup(pageCode,'lxml')
        if not pageCode:
            print "页面加载失败...."
            return None
        title=soup.select('#main > div.col.detailPrimary.mb15 > div.col_sub.mainTitle > h1')
        date=soup.select('li.time')
        price=soup.select('span.price.c_f50')
        pattern = re.compile(r'\d+')
        result = re.findall(pattern,str(title))
        data={
                'title':result[1],
                'date':date[0].text,
                'price':price[0].text,
                'url':url,
                      }
        content_list.insert_one(data)
        print data
pool=Pool()
pool.map(getPageItems())
'''
'#main > div.col.detailPrimary.mb15 > div.col_sub.mainTitle > h1'
#divContacter > ul > ul > li > a
'#t_phone'
#infocont > span > b
#divContacter > ul > ul > li > a
'''