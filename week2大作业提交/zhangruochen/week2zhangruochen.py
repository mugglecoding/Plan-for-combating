from bs4 import BeautifulSoup
import requests
import pymongo
import time

start_page ='http://bj.ganji.com/wu/'
host_url = 'http://bj.ganji.com'

client = pymongo.MongoClient('localhost', 27017)
gjproject = client['gjproject']
gjcate = gjproject['gjcate']
geren_item_list = gjproject['geren_item_list']
shangjia_item_list = gjproject['shangjia_item_list']
item_info = gjproject['item_info']
links=[]

def get_channel_urls(url):
    wb_data = requests.get(url).text
    soup = BeautifulSoup(wb_data, 'lxml')
    links = soup.select('dl.fenlei > dt > a')
    for link in links:
        cate_url = host_url + link.get('href')
        gjcate.insert_one({'cate_url':cate_url})
        print(cate_url)

# get_channel_urls(start_page)


def get_links_from(channel, pages, who_sells):
    # http://bj.ganji.com/jiaju/a2o3/
    list_view = '{}{}o{}/'.format(channel, who_sells, str(pages))
    # print(list_view)
    wb_data = requests.get(list_view)
    time.sleep(1)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    if soup.find('li','js-item'):
        for link in soup.select('a.ft-tit'):
            item_link = link.get("href")
            item_list.insert_one({'url': item_link})
    else:
        pass


def get_item_info():
    for geren_item in geren_item_list.find():
        url = geren_item['url']
        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        title = soup.select('.title-name')[0].text
        price = soup.select('i.f22.fc-orange')[0].get_text()
        date = soup.select('i.pr-5')[0].text.strip()
        area = soup.select('ul.det-infor > li > a[target="_blank"]')[1].get_text()
        type = soup.select('.det-infor > li > span > a[target="_blank"]')[0].get_text()
        if seller_type = u'个人'
        item_info.insert_one({'title':title,'price':price, 'date':date, 'area':area, 'type':type, 'seller_type':seller_type})
        print({'title':title,'price':price, 'date':date, 'area':area, 'type':type, 'seller_type':seller_type})

    for shangjia_item in shangjia_item_list.find():
        url = shangjia_item['url']
        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        title = soup.select('.title-name')[0].text
        price = soup.select('i.f22.fc-orange')[0].get_text()
        date = soup.select('i.pr-5')[0].text.strip()
        area = soup.select('ul.det-infor > li > a[target="_blank"]')[1].get_text()
        type = soup.select('.det-infor > li > span > a[target="_blank"]')[0].get_text()
        seller_type = u'商家'
        item_info.insert_one({'title':title,'price':price, 'date':date, 'area':area, 'type':type, 'seller_type':seller_type})
        print({'title':title,'price':price, 'date':date, 'area':area, 'type':type, 'seller_type':seller_type})


for cate in gjcate.find():
    channel = cate['cate_url']
    for pages in range(0,120):
        get_links_from(channel, pages, who_sells='')
        geren_item_list.insert_one({'url': item_link})
        get_links_from(channel, pages, who_sells='a2')
        shangjia_item_list.insert_one({'url': item_link})

get_item_info()


