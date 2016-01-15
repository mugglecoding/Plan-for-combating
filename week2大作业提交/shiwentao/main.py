#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'stone'

from multiprocessing import Pool
from channel import channel_list
from pages import get_links_from_channel
from pages import get_info_from_url
from pages import url_list


def get_all_links(channel):
    for i in range(1,5):
        get_links_from_channel(channel,i)

def get_info(item):
    if item.get('visited') != 0:
        pass
    else:
        get_info_from_url(item['url'])
        url_list.update_one({'_id':item['_id']},{'$set':{'visited':1}},False,False)



if __name__ == '__main__':
    pool = Pool()
    pool.map(get_all_links,channel_list.split())
    # for item in url_list.find():
    #     items = []
    #     print item
    #     items.append(item)
    #     pool.map(get_info,items)
    for item in url_list.find():
        #print item
        pool.apply_async(get_info,(item,))
    pool.close()
    pool.join()


# for i in range(10):
#     url_list.insert_one({'url':'http://baidu.com'.format(str(1)),'visited':0})
