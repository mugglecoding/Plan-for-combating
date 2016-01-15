#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-01-04 20:52
# @Author  : LeiYue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/
# @Version : $Id$

from __future__ import print_function
import json
import codecs

def main():
    json_file = codecs.open('items.json', 'r', encoding='utf-8')
    data = json_file.read()
    items = json.loads(data)

    for item in items:
        print(item['category'])


if __name__ == '__main__':
    main()
