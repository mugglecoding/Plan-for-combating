# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import sys
import json
sys.stdout=open('output1.txt','w')
from bs4 import BeautifulSoup

#北京二手平板电脑爬虫类
class bjtc:

    #初始化方法，定义一些变量
    def __init__(self):
        #存放二手平板交易信息详情的变量，每一个元素是每一项交易的详情信息
        self.data = {}
    def getPage(self):
        try:
           url = 'http://bj.58.com/pbdn/?PGTID=0d305a36-0000-1c13-dbb5-b90c3352d3d1&ClickID=2'#构建请求的request
           request = urllib2.Request(url)
           response = urllib2.urlopen(request)
           pageCode = response.read().decode('utf-8')
           soup = BeautifulSoup(pageCode,'lxml')
           links =soup.select('td.t > a.t')
           href=[]
           for link in links:
                href.append(link.get('href'))
           return href

        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接58同城失败,错误原因",e.reason
                return None

    #传入交易详情的网址，返回抓取的数据
    def getPageItems(self,herf):
        request = urllib2.Request(herf)
        response = urllib2.urlopen(request)
        pageCode = response.read().decode('utf-8')
        soup = BeautifulSoup(pageCode,'lxml')
        if not pageCode:
            print "页面加载失败...."
            return None
        pattern = re.compile(r'\d+')
        id = re.findall(pattern,herf)
        titles=soup.select('#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.mainTitle > h1')
        counts=self.getPagecount(id[1])
        dates=soup.select('#index_show > ul.mtit_con_left.fl > li.time')
        prices=soup.select('span.price.c_f50')
        atypes=soup.select('#divContacter > ul > ul > li > em')
        if atypes =='':
            types='个人'
        else:
            types='商家'
        areaes=soup.select('div.su_con > span > a')
        aclasses=soup.select('#header > div.breadCrumb.f12 > span:nth-child > a')
#print(titles,counts,dates,prices,types,areaes,classes)

        for title,count,date,price,type,area,classes in zip(titles,counts,dates,prices,types,areaes,aclasses[2]):
                self.data={
                 'title':title.get_text(),
                 'count':count,
                 'date':date.get_text(),
                 'price':price.get_text(),
                 'type':type,
                 'area':list(area.stripped_strings),
                 'aclass':classes,
             }
        return self.data

    #传入交易详情的ID号，返回该商品打浏览次数
    def getPagecount(self,id):
        url='http://jst1.58.com/counter?infoid='+str(id)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        pageCode = response.read().decode('utf-8')
        pattern = re.compile(r'\d+')
        result = re.findall(pattern,pageCode)
        return result[4]


    #开始方法
    def start(self):
        hrefs=self.getPage()
        for href in hrefs:
           self.data= self.getPageItems(href)
           print self.data
           print json.dumps(self.data, encoding='UTF-8', ensure_ascii=False)

spider = bjtc()
spider.start()