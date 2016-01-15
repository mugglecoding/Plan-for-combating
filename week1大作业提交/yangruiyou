#!/usr/bin/python
#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time


url='http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'
wb_data=requests.get(url)

soup=BeautifulSoup(wb_data.text,'lxml')
false_addr=soup.select('.t > a[target="_blank"]')
real_addr1 = [addr.get('href')  for addr in false_addr]
#print real_addr1
real_addr =[ addr1 for addr1 in real_addr1 if addr1[0:16]=='http://bj.58.com']
#real_addr = [addr.get('href')  for addr in false_addr if addr.startswith(addr,1,16)=='http://bj.58.com')]
#print real_addr


for address in real_addr:
  web_data=requests.get(address)
  soup1=BeautifulSoup(web_data.text,'lxml')
  pro_title=soup1.select('div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.mainTitle > h1')
  view_count=soup1.select('ul.mtit_con_left.fl > li.count')
  note_time=soup1.select('ul.mtit_con_left.fl > li.time')
  pro_price=soup1.select('div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li > div.su_con > span')
  bug_type=soup1.select('div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li > div.su_tit')
  area=soup1.select('div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li > div.su_tit')




  #print (pro_title,view_count,note_time,pro_price,bug_type,area)
  for pro_title,view_count,note_time,pro_price,bug_type,area in zip(pro_title,view_count,note_time,pro_price,bug_type,area):
    data={
      'pro_title':pro_title.get_text(),
      'view_count':view_count.get_text(),
      'note_time':note_time.get_text(),
      'pro_price':pro_price.get_text(),
      'bug_type':bug_type.get_text(),
      'area':area.get_text()}
    print (data)
