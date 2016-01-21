#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-01-10 17:16
# @Author  : LeiYue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/
# @Version : $Id$

from __future__ import print_function
import pymongo


def main():
    result = []
    client = pymongo.MongoClient('localhost', 27017)
    database = client['xiaozhu']
    table = database['units']

    for item in table.find({'luPrice': {'$gte': 500}}):
        print(item['luTitle'], item['luPrice'])
        result.append(item)

    print(u'共计 {number} 套住房短期租价大于等于 RMB ￥500'.format(number=len(result)))

'''
"luTitle" : "自助厨房，花园庭院，完美传统民居."
"luPrice" : 6588
'''

if __name__ == '__main__':
    main()
