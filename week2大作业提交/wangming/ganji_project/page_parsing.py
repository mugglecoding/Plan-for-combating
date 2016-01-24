# _*_ coding:utf-8 _*_
import io
import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')     # 改变标准输出的默认编码
from bs4 import BeautifulSoup
import requests
import time
import pymongo

time = time
# mongoDB 数据库初始化准备
client = pymongo.MongoClient('localhost', 27017, connect=False)
test = client['test']
url_list = test['url_list']
item_info = test['item_info']

# 通过频道的输入，得到频道内的所有页面产品信息
def get_url_link(channel, page, who_sells=0):
    # 查询产品详情的链接
    list_url = '{}{}{}'.format(channel, str(who_sells), str(page))
    web_data = requests.get(list_url)
    web_data.encoding = 'utf-8'        # 以utf-8编码输出网页解码内容
    soup =BeautifulSoup(web_data.text, 'lxml')
    time.sleep(2)
    if soup.find('dl'):
        links = soup.select('li.js-item a.ft-tit')
        # print(links)
        for link in links:
            item_link = link.get('href')
            print(item_link)
            url_list.insert_one({'url': item_link})
        else:
            pass

# channel = 'http://bj.ganji.com/shouji/'
# get_url_link(channel, 3)

# 通过商品详细的url，进行商品属性的抓取
def get_item_info(url_item, who_sells=0):
     import time
     web_data = requests.get(url_item)
     web_data.encoding = 'utf-8'        # 以utf-8编码输出网页解码内容
     soup = BeautifulSoup(web_data.text, 'lxml')
     time.sleep(2)

     '''
     # 判断当前url页面是否存在，并给与相应处理机制
     # print(soup.find('p', 'error-tips1'))
     # no_page_exit = '信息刚被删除' in soup.select('.error-tips1')
     '''
     if soup.find('p', 'error-tips1') != None:
         # print('pass')
         pass
     else:
         title = soup.title.text
         price = soup.select('.f22')[0].text
         time = soup.select('.pr-5')[0].text.strip().split('\xa0')[0]
         type = '个人'if who_sells == 0 else '商家'
         area_list = soup.select('ul.det-infor > li > a')
         area = ''
         for area_num in area_list:
             if area_num == area_list[-1]:
                area = area + area_num.text
             else:
                 area = area + area_num.text + '-'


         data = {
             'title': title, 'time': time, 'price': price, 'type': type, 'area': area
         }
         print(data)
         item_info.insert_one(data)

# get_item_info('http://wx.ganji.com/shouji/1933464403x.htm')

# get_item_info('http://bj.ganji.com/shouji/1933765975x.htm')
