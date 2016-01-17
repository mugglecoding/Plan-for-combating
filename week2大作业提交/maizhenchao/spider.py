from bs4 import BeautifulSoup
import requests, time, pymongo

client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
url_list = ganji['url_list']
item_info = ganji['item_info']
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER',
    'Cookie':'statistics_clientid=me; citydomain=bj; ganji_uuid=2711949996281942017378; ganji_xuuid=e8415810-48bf-419f-bfa3-7bb0527d2a02.1452610636043; GANJISESSID=9517ae6745774f3fa6bdf72e0d33ffe8; __utmt=1; lg=1; __utma=32156897.1795216929.1452610633.1452706623.1452776027.5; __utmb=32156897.15.10.1452776027; __utmc=32156897; __utmz=32156897.1452615945.2.2.utmcsr=bj.ganji.com|utmccn=(referral)|utmcmd=referral|utmcct=/wu/; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A75226686335%7D'
}

def get_link(channel, page, seller_num):
    url = channel + 'a{}'.format(str(seller_num)) + 'o{}/'.format(str(page))
    web = requests.get(url, headers=headers)
    time.sleep(2)
    soup = BeautifulSoup(web.text, 'lxml')
    if soup.find('a',class_='next'):
        links = soup.select('.ft-tit')
        seller_type = u'个人' if seller_num == 1 else u'商家'
        for link in links:
            url_list.insert_one({'url':link.get('href'), 'seller_type':seller_type})

def get_info(url,seller_type):
    web = requests.get(url,headers=headers)
    time.sleep(2)
    soup = BeautifulSoup(web.text, 'lxml')
    if soup.find('p',class_='error-tips1'):
        pass
    else:
        title = soup.select('.title-name')[0].text
        date = ' '.join(soup.select('.pr-5')[0].text.split()[:2])
        price = soup.select('.f22')[0].text

        areas = soup.select('ul.det-infor > li:nth-of-type(3) > a')
        adds = [area.text for area in areas]
        add = '-'.join(adds)

        types = soup.select('ul.det-infor > li:nth-of-type(1) > span > a')
        item_types = [i.text for i in types]
        item_type = '-'.join(item_types)

        info = {'title': title, 'date': date, 'price': price, 'address': add, 'item_type': item_type, 'url': url, 'seller_type': seller_type}
        item_info.insert_one(info)
        print(info)

