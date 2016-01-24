#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-01-10 11:52
# @Author  : LeiYue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/
# @Version : $Id$

from __future__ import print_function

import json
import re
import time

import pymongo
import requests

USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) ' \
             'AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 ' \
             'Mobile/12A4345d Safari/600.1.4'

COOKIE = 'abtest_ABTest4SearchDate=b; ' \
         '__utmt=1; ' \
         'OZ_1U_2282=vid=v687bcdc624ccf.0&ctime=1452396673&ltime=1452396659; ' \
         'OZ_1Y_2282=erefer=-&eurl=http%3A//bj.xiaozhu.com/search-duanzufang-p1-0/&etime=1452396218&ctime=1452396673&ltime=1452396659&compid=2282; ' \
         'startDate=2016-01-10; ' \
         'endDate=2016-01-11; ' \
         '__utma=29082403.615837787.1452396220.1452396220.1452396220.1; ' \
         '__utmb=29082403.16.10.1452396220; ' \
         '__utmc=29082403; ' \
         '__utmz=29082403.1452396220.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ' \
         'OZ_1U_2283=vid=v687bd8498dba5.0&ctime=1452396758&ltime=1452396734; ' \
         'OZ_1Y_2283=erefer=-&eurl=http%3A//m.xiaozhu.com/search.html%3Fcityid%3D12%26city%3D%2525E5%25258C%252597%2525E4%2525BA%2525AC%26offset%3D25%26step%3D15%26st%3D2016-01-10%26et%3D2016-01-11%26&etime=1452396413&ctime=1452396758&ltime=1452396734&compid=2283'

REFERER = 'http://m.xiaozhu.com/search.html?' \
          'cityid=12&' \
          'city=%25E5%258C%2597%25E4%25BA%25AC&' \
          'sort=zuigui&' \
          'offset=1&' \
          'step=15&' \
          'st=2016-01-10&' \
          'et=2016-01-11&'

HEADERS = {
    'User-Agent': USER_AGENT,
    'Cookie'    : COOKIE,
    'Referer'   : REFERER,
}

OFFSET = 0
LENGTH = 500
MIN_PRICE = 499

URL = 'http://wireless.xiaozhu.com/app/xzfk/html5/201/search/result?jsonp=api_search_result&' \
      'cityId=12&' \
      'offset={offset}&' \
      'length={length}&' \
      'orderBy=zuigui&' \
      'minPrice={minPrice}&' \
      'userId=0&' \
      'sessId=0&' \
      'jsonp=api_search_result&' \
      'timestamp={timestamp}7'.format(offset=OFFSET, length=LENGTH, minPrice=MIN_PRICE,
                                      timestamp=int(round(time.time()*1000)))

'''
'http://wireless.xiaozhu.com/app/xzfk/html5/201/search/result?jsonp=api_search_result&' \
      'cityId=12&' \
      'offset={offset}&' \
      'length={length}&' \
      'orderBy=zuigui&' \
      'checkInDay=&' \
      'checkOutDay=&' \
      'leaseType=&' \
      'minPrice={minPrice}&' \
      'maxPrice=&' \
      'distId=&' \
      'locId=&' \
      'keyword=&' \
      'huXing=&' \
      'facilitys=&' \
      'guestNum=&' \
      'userId=0&' \
      'sessId=0&' \
      'jsonp=api_search_result&' \
      'timestamp=1452396770527&' \
      '_=1452396733429'.format(offset=OFFSET, length=LENGTH, minPrice=MIN_PRICE)
'''


def get_items(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(u'爬取数据出现错误，错误代码：' + str(response.status_code))
        return None
    pattern = re.compile(r'api_search_result\((.*)\)')
    result = re.sub(pattern, r'\1', response.text)
    print(u'获取数据成功，正在处理数据……')
    units = json.loads(result)['content']['item']
    return units


def main():
    client = pymongo.MongoClient('localhost', 27017)
    database = client['xiaozhu']
    table = database['units']
    print(u'正在从以下地址读取数据：' + URL)
    items = get_items(URL)
    print(u'总共获取了 {number} 项数据.'.format(number=len(items)))

    # with open('items.json', 'w') as f:
    #     json.dump(items, f)

    print(u'正在将数据导入数据库中……')
    for item in items:
        table.insert_one(item)
    print(u'数据导入完毕。')


if __name__ == '__main__':
    main()
