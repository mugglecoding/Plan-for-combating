#encoding:utf-8
from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost',27017)
ganji = client['ganji']
url_list = ganji['url_list']
url_list_vip = ganji['url_list_vip']
item_info = ganji['item_info']
item_info_vip = ganji['item_info_vip']

# 爬虫1：获取全部的抓取页面的url地址
def get_links_from(channel,pages,who_sells='o'):
    list_view = '{}{}{}'.format(channel,who_sells,str(pages))
    wb_content = requests.get(list_view)
    time.sleep(3)
    soup = BeautifulSoup(wb_content.text,'lxml')
    if soup.find('div','pageBox'):
        for link in soup.select('a.ft-tit'):
            item_link = link.get('href')
            if(who_sells=='o'):
                url_list.insert_one({'url':item_link})
            elif(who_sells=='a'):
                url_list_vip.insert_one({'url':item_link})

def get_item_info_from(url):
    wb_content = requests.get(url)
    time.sleep(3)
    soup = BeautifulSoup(wb_content.text,'lxml')
    no_longer_exist = soup.find('div.error')
    if no_longer_exist:
        pass
    else:
        title = soup.select('h1.title-name')[0].text
        publish_time = soup.select('i.pr-5')[0].text.split('发布')[0].split() if soup.find_all('i','pr-5') else None
        item_type = soup.select('ul.det-infor li span a')[0].text.split()
        price = soup.select('i.f22.fc-orange.f-type')[0].text
        area = list(soup.select('ul.det-infor li:nth-of-type(3)')[0].stripped_strings)[1:10]
        seller_types = soup.select('span.fc-orange')[0].text
        if '个人' in seller_types:
            seller_type = '个人'
            item_info.insert_one({'title':title,'time':publish_time,'itype':item_type,'price':price,'area':area,'stype':seller_type})
        else:
            seller_type = '商家'
            item_info_vip.insert_one({'title':title,'time':publish_time,'itype':item_type,'price':price,'area':area,'stype':seller_type})

if __name__=="__main__":
    get_links_from('http://bj.ganji.com/rirongbaihuo/',3)
    get_links_from('http://bj.ganji.com/rirongbaihuo/',3,'a')
    get_item_info('http://bj.ganji.com/rirongbaihuo/1437873732x.htm')