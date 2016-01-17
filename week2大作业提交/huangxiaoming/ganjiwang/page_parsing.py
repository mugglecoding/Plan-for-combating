from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost',27017)
ganji = client['ganji']
ganji_links = ganji['ganji_links']
ganji_item = ganji['ganji_itme']

#spider1 抓取一般商品链接
def get_links_from(channel,page,who_sell):
    url_link = '{}a{}o{}/'.format(channel,who_sell,str(page))
    #url_link = 'http://bj.ganji.com/jiaju/o3/'
    web_data = requests.get(url_link)
    soup = BeautifulSoup(web_data.text,'lxml')
    time.sleep(1)
    if soup.find('div','pageBox'):
        item_links = soup.select('a.ft-tit')
        for item_link in item_links:
            url = item_link.get('href').split('?')[0]
            ganji_links.insert_one({'url':url})
            # print(url)
    else:
        pass
# get_links_from('http://bj.ganji.com/shouji/',1,2)


#spider2 爬取商品信息
def get_item_info(item_url):
    web_data = requests.get(item_url)
    soup = BeautifulSoup(web_data.text,'lxml')
    time.sleep(1)
    if soup.find('div','error'):
        pass
    else:
        title = soup.select('h1.title-name')[0].text
        price = soup.select('i.f22')[0].text
        type = list(soup.select('ul.det-infor li:nth-of-type(1) span')[0].stripped_strings)
        area = list(soup.select('ul.det-infor li:nth-of-type(3)')[0].stripped_strings)
        del area[0] #删除列表第一项'交易地点'
        date = soup.select('i.pr-5')[0].text.split('发布')[0].split() if soup.find('i','pr-5') else None #卖家为商家时，无发布时间
        seller_type = soup.select('span.fc-orange')[0].get_text()
        if seller_type == '':
            seller_type = '个人'
        else:
            seller_type = '商家'
        # print({'title':title,'price':price,'type':type,'area':area,'date':date,'seller_type':seller_type})
        ganji_item.insert_one({'title':title,'price':price,'type':type,'area':area,'date':date,'seller_type':seller_type})
# get_item_info('http://bj.ganji.com/shouji/2071745684x.htm')

