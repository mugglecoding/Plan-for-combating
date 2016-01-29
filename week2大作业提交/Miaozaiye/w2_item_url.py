from bs4 import BeautifulSoup
import requests
import time
from w2_channel_extract import caturl,category
import pymongo
import random
from multiprocessing import Pool




client = pymongo.MongoClient('localhost',27017)
ganji = client['ganji']
test = ganji['test']
detail1 = ganji['detail1']
item_urls1 = ganji['item_urls1']
item_url = []


headers = {
    'UserAgent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'connection':'keep-Alive'

}


proxy_list = [
    'http://117.117.250.151:0001',
    'http://111.85.219.250:3129',
    'http://122.70.183.138:8118'
]
proxy_ip = random.choice(proxy_list)
proxies = {'http':proxy_ip}


def get_itemurl(channel_url,category,sellertype = 'o'): #默认是个人类型,商家类型则sellertype = 'a'
    i = 1                                              #从第1页开始取链接
    itemurllist = []                           #给列表设一个表首,标记种类
    while True:                                        #为之后的条件跳出做准备
        url = channel_url+sellertype+str(i)
        print ('item url: ',url)
        wb_data = requests.get(url,headers = headers,proxies = proxies)
        wb_data.encoding = 'utf-8'
        soup = BeautifulSoup(wb_data.text,'lxml')

        if soup.find_all('div','pageBox'):  #如果找到商品的时间标签,则证明该页是正常页面,可以正常抽取链接.
            print ('True')

            itemurls = soup.select('a.ft-tit') #找到商品链接组
            for item in itemurls :             #将商品链接从链接组里面拆分出来,拆分出链接信息,放入itemurllist,备用
                itemurl = item.get('href')
                print (itemurl)
                item_urls1.insert_one({'category':category, 'link':itemurl})
                print (ganji.item_urls1.find().count())
            i = i+1                           #翻页
            print ('page : ',i)




        else:                              #如果找不到商品的时间标签,则证明该页非正常页面,跳出不再读取数据.

            print('False')
            break


print (caturl)
caturl.remove('http://bj.ganji.com/shoujihaoma/')
category.remove('手机号码')


def get_all_links(url):
     get_itemurl(url,url.split('/')[-2])

for url in caturl:
    print (url)
    get_all_links(url)


'''
def get_itemdetail(url):                   #获取指定链接的产品信息
    wb_data = requests.get(url)
    wb_data.encoding = 'utf-8'
    soup = BeautifulSoup(wb_data.text,'lxml')
    # print (soup)
    print (url)

    if '赶集 转转详情页' in soup.title:
        pass
    elif soup.find_all('div','error'):
        pass
    else:
        title = soup.title.get_text()
        date = soup.select('i.pr-5')[0].get_text().strip().split('\xa0')[0] if soup.find_all('i','pr-5') else None
        price = soup.select('i.f22.fc-orange.f-type')[0].get_text() if soup.find_all('i','f22 fc-orange f-type') else None

        type = soup.select('ul.det-infor > li > span > a')[0].get_text()
        address = soup.select('#wrapper > div.content.clearfix > div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(3) > a')
        address0 = [address[i].get_text()for i in range(0,len(address))]
        item_detail = {'title':title,'date':date,'price':price,'type':type,'address':address0,'url':url}
        print (ganji.detail1.find().count())
        detail1.insert_one(item_detail)       #将产品信息插入到数据库中




for link in item_url:
    get_itemdetail(link)

'''
