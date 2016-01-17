from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost',27017)#建立与mongoDB联系
ganji = client['ganji']
ganji_links = ganji['ganji_links']#建立数据表,存储商品链接
ganji_item = ganji['ganji_itme']#建立数据表,存储商品信息

#spider1 抓取一般商品链接
def get_links_from(channel,page,who_sell):
    url_link = '{}{}o{}/'.format(channel,who_sell,str(page))
    #url_link = 'http://bj.ganji.com/jiaju/o3/'
    web_data = requests.get(url_link)
    soup = BeautifulSoup(web_data.text,'lxml')
    time.sleep(1)
    if soup.find_all('div','pageBox'):

        item_links = soup.select('a.ft-tit')
        for item_link in item_links:
            url = item_link.get('href')
            ganji_links.insert_one({'url':url})
            print(url)
    else:
        pass
#spider2 爬取商品信息
def get_item_info(item_page):
    web_data = requests.get(item_page)
    soup = BeautifulSoup(web_data.text,'lxml')
    time.sleep(1)
    no_item_exist = soup.select('div error')#当页面不存在时，直接跳过
    if no_item_exist:
        pass
    else:
        title = soup.select('h1.title-name')[0].text
        publish_time = soup.select('i.pr-5')[0].text.split('发布')[0].split() if soup.find_all('i','pr-5') else None#卖家为商家时，无发布时间一栏
        item_type = soup.select('ul.det-infor li span a')[0].text.split()
        price = soup.select('i.f22.fc-orange.f-type')[0].text
        area = list(soup.select('ul.det-infor li:nth-of-type(3)')[0].stripped_strings)[1:10]
        seller_type = soup.select('span.fc-orange')[0].text
        if '商家' in seller_type:
            stype = '商家'
        else:
            stype = '个人'
        ganji_item.insert_one({'title':title,'time':publish_time,'itype':item_type,'price':price,'area':area,'stype':stype})


# get_item_info('http://bj.ganji.com/jiaju/1475537716x.htm')

#get_links_from('http://bj.ganji.com/jiaju/',4,who_sell='a2')
