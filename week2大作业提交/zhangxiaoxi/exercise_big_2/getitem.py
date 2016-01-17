# -*- coding:utf-8 -*-
import urllib2
import pymongo
from bs4 import BeautifulSoup
from multiprocessing import Pool
client =pymongo.MongoClient('localhost',27017)
walden=client['ganjiwang']
url_list=walden['url_list']
content_list=walden['content_list']
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/47.0.2526.106 Chrome/47.0.2526.106 Safari/537.36'
headers = { 'User-Agent' : user_agent }
def getPageItems():
    for href in content_list.find({}, {'url' : 1}):
       if href in url_list.find({}, {'url' : 1}):
           print  '已抓取过'
       else:
        url=href.get('url')
        request = urllib2.Request(url,headers = headers)
        response = urllib2.urlopen(request)
        pageCode = response.read().decode('utf-8')
        soup = BeautifulSoup(pageCode,'lxml')
        if not pageCode:
            print "页面加载失败...."
            return None
        title=soup.select('h1.title-name')
        date=soup.select('i.pr-5')
        price=soup.select('i.f22.fc-orange.f-type')
        area=soup.select('#wrapper > div.content.clearfix > div.leftBox > div:nth-child > div > ul > li:nth-child > a')
        areas=[]
        for i in range(1,4):
            areas.append(area[i].text)
        atypes=soup.select('span.fc-orange')
        if atypes =='':
            type='个人'
        else:
            type='商家'
        data={
                'title':title[0].text,
                'date':date[0].text,
                'price':price[0].text,
                'area':areas,
                'type':type,
                'url':url,
                      }
        content_list.insert_one(data)
        print data
'''
'#main > div.col.detailPrimary.mb15 > div.col_sub.mainTitle > h1'
#divContacter > ul > ul > li > a
'#t_phone'
#infocont > span > b
#wrapper > div.content.clearfix > div.leftBox > div:nth-child(3) > div > ul > li > a
div.det-laybox>ul.det-infor> li:nth-child(3)>a
#divContacter > ul > ul > li > a
'''