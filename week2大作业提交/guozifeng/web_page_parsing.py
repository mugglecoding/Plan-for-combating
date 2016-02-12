#coding = utf-8
from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost',27017)
project_market = client['project_market']
url_list = project_market['url_list']
item_info = project_market['item_info']

def get_links_from(link,pages,who_type=1):
    url = '{}a{}o{}/' .format (link, str(who_type),str(pages))
    #url = 'http://bj.ganji.com/jiaju/a1o1/'
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    if soup.find('div','pageBox'):
        for link in soup.select('.ft-tit'):
            item_link = link.get('href')
            url_list.insert_one({'url':item_link})
            print(item_link)
    else:
        return

def get_item_info(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    if soup.find('h1','title-name'):
        title = soup.select('.title-name')[0].text.split('-')[0]
        post_time = soup.select('.pr-5')[0].text.strip().split(' ')[0]
        type_info = soup.select('div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(1) > span > a')[0].text
        price = soup.select('.f22')[0].text
        area = list(map(lambda x:x.text,soup.select('div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(3) > a ')))
        data = {
            '商品标题':title,
            '发帖时间':post_time,
            '类型':type_info,
            '价格':price,
            '交易地点':area,
            'url':url
        }
        print(data)
        item_info.insert_one(data)

    else:
        pass

# url = 'http://biz.click.ganji.com/bizClick?url=pZwY0jCfsvFJshI6UhGGshPfUiqJpy7JIitQPHEYP1nOrH9vXaOCIAd0njTQPDDzn1cvwDndnHn3ENRjnbFAnHwanNDknH03rH0zwNP0njTQPjEdPWT3nWTdn1DdnjE3rHnzPHbvndkknjDVgjTknHELnjbQPHEQn7kknjDQP7kknjDQPHEYP1nOrH9vgjTknHDQn7kknjDvndkknjDQPj60njTQnHF0njTQnHEdPHD3rHcvnWmkPdkknjDQgjTknHD1nRkknj7BpywbpyOMgjTknH70njTQuv78ph-WUvdx0AI0njTQn7kknjDYPjNvnj9znjN1nHNkPj9On1cdrHm1gjTknHK0njTQnWc1sW01sWE3sW0OgjTknNdfXh-_UADfPi3kca6gpyObULI1cDONcjDksWTec7I5R1mY2iKK0ZK_uRI-mbVGIatdn108n1m92DVcRDdnsaK_pyV-cDI-mvVf2iKjpZFfUyNfPj98na3zPHmYsWbLc7P6uh7zpitdn108n1u0njTQPH9YgjTkniYQgjTkniYQgjTknNPC0hqVuE&v=2'
#url = 'http://bj.ganji.com/jiaju/1956529909x.htm'
#get_item_info(url)