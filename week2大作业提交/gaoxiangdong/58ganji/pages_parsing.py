from bs4 import BeautifulSoup
import requests
import time
import pymongo

headers = {
     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4',
     'Cookie': 'citydomain=bj; ganji_xuuid=1879886f-c902-44ec-89eb-ab28e0b0478a.1452608110409; ganji_uuid=5212120881512590752584; GANJISESSID=56073313f2a81dab106991dfbdffa334; hotPriceTip=1; STA_DS=0; lg=1; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A80111296479%7D; __utma=32156897.1500200464.1452608104.1452608104.1452696203.2; __utmb=32156897.17.10.1452696203; __utmc=32156897; __utmz=32156897.1452608104.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'

}
client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
url_list = ganji['url_list']
item_info = ganji['item_info']
# url_list.remove({})
# item_info.remove({})


def get_links_from(channel, page, who_sell='o'):
    url = '{}{}{}/'.format(channel, who_sell, str(page),)
    print(url)
    print(url_list.find().count())
    time.sleep(3)
    requests.adapters.DEFAULT_RETRIES = 5
    wb_data = requests.get(url,)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    links = soup.select('#wrapper > div.leftBox > div.layoutlist > dl')
    links_length = links.__len__()
    if who_sell == 'o':
        seller_type = '个人'
    else:
        seller_type = '商家'

    if links_length > 10:

        for link in links:
            url_list.insert_one({'link':link.find('a').get('href'),'seller_type':seller_type})
            # print(link.find('a').get('href'))




def get_item_info(url_info):
    time.sleep(3)
    print( item_info.find().count())
    print(url_info['link'])
    print(url_info['seller_type'])
    wb_data = requests.get(url_info['link'])
    # wb_data = requests.get(url_info)
    soup = BeautifulSoup(wb_data.text , 'lxml')
    error = soup.select('div.cont-right > div > p.error-tips1')
    if error.__len__() > 0:
        print('error')
    else :
        title = soup.select(' div.col-cont.title-box > h1')[0].get_text()
        release_time = soup.select('ul.title-info-l.clearfix > li:nth-of-type(1) > i')[0].get_text().strip().strip('发布')
        price = soup.select('i.f22.fc-orange.f-type')[0].get_text()
        areas = soup.select('div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(3)')
        area = list(areas[0].stripped_strings)
        types = soup.select('div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(1) > span ')
        type = list(types[0].stripped_strings)
        print('time',release_time)
        print('title',title)
        print('price', price)
        print('area', area)
        print('type', type)
        item_info.insert_one({'title': title, 'release_time': release_time, 'price': price, 'type': type, 'seller_type': url_info['seller_type']})


# get_links_from('http://bj.ganji.com/ershoubijibendiannao/', 3,'a')
# get_item_info('http://bj.ganji.com/jiaju/1897471045x.htm')



