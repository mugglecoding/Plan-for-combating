#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-01-10 12:24
# @Author  : LeiYue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/
# @Version : $Id$


import os.path

import pymongo


def connect():
    client = pymongo.MongoClient('localhost', 27017)
    database = client['walden']
    table = database['content']

    return table


def insert_data(table):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(base_dir, 'walden.txt')
    with open(path, 'r') as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            data = {
                'index': index,
                'line' : line,
                'words': len(line.split()),
            }
            table.insert_one(data)


def get_data(table):
    for item in table.find({'words': 0}):
        print item


def main():
    table = connect()
    # insert_data(table)
    get_data(table)


if __name__ == '__main__':
    main()
