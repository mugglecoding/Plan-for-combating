#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-01-03 12:14
# @Author  : LeiYue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/
# @Version : $Id$

from __future__ import print_function
import requests
import time
import json

LIMIT = 20
URL = 'http://movie.douban.com/j/search_subjects?type=movie&tag=%E7%A7%91%E5%B9%BB&sort=recommend&page_limit={limit}&page_start={start}'

def getPages(start, end):
    items = []
    for page in range(start, end):
        time.sleep(4)
        pageItems = getItems(URL.format(limit=LIMIT, start=page*20))
        items.extend(pageItems)
    return items


def getItems(url):
    items = []
    print('正在爬取数据……')
    response = requests.get(url)
    if response.status_code != 200:
        print('爬取数据出现错误，错误代码：'+str(response.status_code))
        return None
    subjects = json.loads(response.text)['subjects']
    for subject in subjects:
        item = {
            'title': subject['title'],
            'cover': subject['cover'],
            'url': subject['url'],
            'rate':subject['rate']
        }
        items.append(item)
    return items

def main():
    items = getPages(0, 5)
    for item in items:
        for key in item.keys():
            print(key, ':', item[key])
        print('-'*80)
    print('总共爬取了', len(items), '项数据……')
    # 好像总共也就80项数据


if __name__ == '__main__':
    main()

