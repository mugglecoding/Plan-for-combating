# coding=gbk
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')


from bs4 import BeautifulSoup
import time
import requests
import pymongo

client = pymongo.MongoClient('localhost', 27017)
database = client['database']
url_list = database['url_list']
item_info = url_list['item_info']

# spider 1
def get_link_from(o_url, who, page):
    url = o_url + 'a{}'.format(str(who)) + 'o{}/'.format(str(page))
    wb_data = requests.get(url)
    time.sleep(1)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    for link in soup.select('a.ft-tit'):
            item_link = link.get('href').split('?')[0]
            url_list.insert_one({'url': item_link})
            #print(item_link)

#get_link_from('http://bj.ganji.com/jiaju/','1','1')
# spider 2
def get_item_info(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    no_longer_exist = '404' in soup.find('script', type="text/javascript").get('src').split('/')
    if no_longer_exist:
        pass
    else:
        title = soup.title.text
        type = soup.select('#wrapper > div.content.clearfix > div.leftBox > div > div > ul > li:nth-child(1) > span > a')
        price = soup.select('#wrapper > div.content.clearfix > div.leftBox > div > div > ul > li:nth-child(2) > i.f22.fc-orange.f-type')[0].text
        date = soup.select('#wrapper > div.content.clearfix > div.leftBox > div.col-cont.title-box > div > ul.title-info-l.clearfix > li > i')[0].text
        area = list(soup.select('#wrapper > div.content.clearfix > div.leftBox > div > div > ul > li'))
        item_info.insert_one({'title': title, 'price': price, 'type':type, date:'date',area:'area',url:'url'})
        print({'title': title, 'price': price,'type':type, 'date': date, 'area': area, 'url': url})