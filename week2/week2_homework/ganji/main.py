#!/usr/bin/env python
#-*- coding: utf-8 -*-

from multiprocessing import Pool
from page_parsing import get_item_info_from, url_list, item_info, get_links_from
from channel_extracing import channel_list

db_urls = [item['url'] for item in url_list.find()]
index_urls = [item['url'] for item in item_info.find()]
x = set(db_urls)
y = set(index_urls)
rest_of_urls = x-y

def get_all_links_from(channel):
     for i in range(1, 100):
         get_links_from(channel, i)


if __name__ == '__main__':
    pool = Pool(processes=6)
    # pool.map(get_all_links_from, channel_list) # 抓取所有商品链接(只需抓一次，此处未支持断点功能)
    pool.map(get_item_info_from, rest_of_urls) # 抓取商品详情页
    pool.close()
    pool.join()
