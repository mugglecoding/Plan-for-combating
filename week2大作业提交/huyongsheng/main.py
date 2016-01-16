#encoding:utf-8
from multiprocessing import Pool
import pymongo
from page_parsing import *
from channel_extract import channel_urls

client = pymongo.MongoClient('localhost',27017)
ganji = client['ganji']
url_list = ganji['url_list']
url_list_vip = ganji['url_list_vip']
item_info = ganji['item_info']
item_info_vip = ganji['item_info_vip']

def get_all_links_from(channel):
    for num in range(1,5):
        if channel.split('/')[-2] == 'shoujihaoma':
            pass
        else:
            get_links_from(channel,num,'a')
            get_links_from(channel,num,'o')

def get_all_item_info(url):
    get_item_info_from(url)

if __name__=="__main__":
    pool = Pool()
    pool.map(get_all_links_from,channel_urls.split())
    for url in ganji['url_list'].find():
        page = url['url'].split()
        pool.map(get_all_item_info,page)
    for url in ganji['url_list_vip'].find():
        page = url['url'].split()
        pool.map(get_all_item_info,page)
    pool.close()