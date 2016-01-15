#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-01-02 20:12
# @Author  : LeiYue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/
# @Version : $Id$

from __future__ import print_function
import requests
import re
import time
import json
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4'
COOKIE = 'abtest_ABTest4SearchDate=b; OZ_1U_2283=vid=v687bd8498dba5.0&ctime=1451738580&ltime=1451738580; OZ_1Y_2283=erefer=-&eurl=http%3A//m.xiaozhu.com/search.html%3Fcityid%3D12%26city%3D%2525E5%25258C%252597%2525E4%2525BA%2525AC%26offset%3D1%26step%3D15%26st%3D2016-01-02%26et%3D2016-01-03%26&etime=1451736646&ctime=1451738580&ltime=1451738580&compid=2283; OZ_1U_2282=vid=v687bcdc624ccf.0&ctime=1451741406&ltime=1451741069; OZ_1Y_2282=erefer=-&eurl=http%3A//bj.xiaozhu.com/search-duanzufang-p1-0/&etime=1451736283&ctime=1451741406&ltime=1451741069&compid=2282; startDate=2016-01-02; endDate=2016-01-03'
REFERER = 'http://m.xiaozhu.com/search.html?cityid=12&city=%25E5%258C%2597%25E4%25BA%25AC&offset=1&step=15&st=2016-01-02&et=2016-01-03&'
HEADERS = {'User-Agent': USER_AGENT, 'Cookie': COOKIE, 'Referer': REFERER}
NUMBER = 300
URL = 'http://wireless.xiaozhu.com/app/xzfk/html5/201/search/result?jsonp=api_search_result&cityId=12&offset=0&length=%s&orderBy=recommend&checkInDay=&checkOutDay=&leaseType=&minPrice=0&maxPrice=&distId=&locId=&keyword=&huXing=&facilitys=&guestNum=&userId=0&sessId=0&jsonp=api_search_result&timestamp=%s'%(str(NUMBER), str(int(round(time.time()*1000))))

def getItems(url):
    items = []
    print('开始爬取数据……')
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print('爬取数据出现错误，错误代码：'+str(response.status_code))
        return None
    pattern = re.compile('api_search_result\((.*)\)')
    result = re.sub(pattern, r'\1', response.text)
    print('获取数据成功，正在处理数据……')
    units = json.loads(result)['content']['item']
    for index, unit in enumerate(units):
        item = {
            'title': unit['luTitle'],
            'image': unit['luMainImageUrl'],
            'address': unit['displayAddr'],
            'price': unit['luPrice'],
            'id': unit['landlordId'],
            'sex': getPerson(unit['landlordId']),
            'name': unit['landlordName'],
            'avatar': unit['landlordheadimgurl']
        }
        items.append(item)
        print('第%s个数据成功处理，请等待……'%str(index+1))
    return items

def getPerson(landlordId):
    response = requests.get('http://www.xiaozhu.com/fangdong/' + str(landlordId)+'/')
    soup = BeautifulSoup(response.text, 'lxml')
    sex = soup.select('body > div.contentFD > div.left_sider.clearfix > div.person_infor > ul.fd_person > li')
    if len(sex):
        return list(sex[0].get_text())[3]
    else:
        return '未知'


def main():
    items = getItems(URL)
    for item in items:
        for key in item.keys():
            print(key, ':', item[key])
        print('-'*80)
if __name__ == '__main__':
    main()
