# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time
import json
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
j=1
url = 'http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'
mb_data = requests.get(url)
soup = BeautifulSoup(mb_data.text, 'lxml')
locationurls = soup.select('a[class="t"]')
info=[]
def web58_prase(url):
    global j
    web_data= requests.get(url)
    soup= BeautifulSoup(web_data.text,'lxml')
    category = soup.select('#header > div.breadCrumb.f12 > span:nth-of-type(3) > a')[0].text
    title= soup.select('h1')[0].text
    post_time= soup.select('li.time')[0].text
    price= soup.select('span.price.c_f50')[0].text
    area= u'未指定' if soup.select('span.c_25d > a:nth-of-type(1)')==[] else soup.select('span.c_25d > a:nth-of-type(1)')[0].text
    type = u'个人' if  soup.select('span[class="red"]')[0].text.lstrip()==''  else u'商家'
    print(u'%d,类目:%s, 标题:%s, 发布时间:%s, 价格:%s 卖家类型:%s 地区:%s' % (j,category, title, post_time, price, type, area))
    j=j+1

for locationurl in locationurls:
    url = locationurl.get('href')
    web58_prase(url)





