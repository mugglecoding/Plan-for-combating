# -*- coding:utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/47.0.2526.106 Chrome/47.0.2526.106 Safari/537.36'
headers = { 'User-Agent' : user_agent }
def getPageItems():
        url='http://bj.ganji.com/ershoubijibendiannao/1893551128x.htm'
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
        print data

getPageItems()