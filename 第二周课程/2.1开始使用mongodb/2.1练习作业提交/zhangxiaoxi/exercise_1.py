# -*- coding:utf-8 -*-
import urllib2
import pymongo
from bs4 import BeautifulSoup
client =pymongo.MongoClient('localhost',27017)
walden=client['walden']
sheet_tab=walden['sheet_tab']
#小猪短租爬虫类
class xzdz:


    def getPage(self):
        pages = []
        for page in range(1,4):
             pages.append('http://bj.xiaozhu.com/search-duanzufang-p' + str(page)+ '-0/')
        return pages

    def getPageItems(self):
        hrefs=self.getPage()
        for href in hrefs:
            request = urllib2.Request(href)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            soup = BeautifulSoup(pageCode,'lxml')
            if not pageCode:
                print "页面加载失败...."
                return None
            titles=soup.select('div > a > span')
            prices=soup.select('span.result_price > i')
            for title,price in zip(titles,prices):
                 data={
                     'title':title.get_text(),
                    'price':price.get_text(),
                      }
                 print data
                 sheet_tab.insert_one(data)

spider = xzdz()
spider.getPageItems()
'''
#page_list > ul > li:nth-child(1) > div.result_btm_con.lodgeunitname > div > a > span
#page_list > ul > li:nth-child(1) > div.result_btm_con.lodgeunitname > span.result_price > i

'''