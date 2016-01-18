# __author__ = 'xjlin'
# -*- coding: utf-8 -*-
from multiprocessing import Pool
import page_parsing
from  channel_extract import channel
import pymongo

client = pymongo.MongoClient('localhost', 27017, maxPoolSize = 50)
ganji = client['ganji']
url_list = ganji['url_list']
item_info = ganji['item_info']
def get_all_links_from(channel):
    for num in range(1,5):
        if channel.split('/')[-2] == 'shoujihaoma':
             page_parsing.get_plink_from(channel, num, 'a1')
             print('crawling url')
             page_parsing.get_plink_from(channel, num, 'a2')
             print('crawling url')
        else:
             page_parsing.get_link_from(channel, num, 'a1')
             print('crawling url')
             page_parsing.get_link_from(channel, num, 'a2')
             print('crawling url')

def get_all_info_from(url):
    key = url.split('/')
    if key[3] == 'shoujihaoma':
        page_parsing.get_pnumber_info(url)
    else:
        page_parsing.get_item_info(url)



if __name__ == '__main__':
    pool = Pool()
    pool.map(get_all_links_from, channel.split())
    for url in ganji['url_list'].find():
        url = url['url']
        print('crawling item info')
        pool.map(get_all_info_from, url.split())