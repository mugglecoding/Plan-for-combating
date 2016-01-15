#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-01-02 16:16
# @Author  : LeiYue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/
# @Version : $Id$

from __future__ import print_function
from bs4 import BeautifulSoup
import re


def main():
    items = []
    pattern = re.compile('(\d+) .*')
    with open('index.html', 'r') as web_data:
        soup = BeautifulSoup(web_data, 'lxml')
        # print(soup.prettify())
        names = soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4 > a')
        images = soup.select('body > div > div > div.col-md-9 > div > div > div > img')
        views = soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p.pull-right')
        prices = soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4.pull-right')
        rates = soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings')
        # print(names, images, views, prices, rates, sep='\n'+'-'*80+'\n')

    for name, image, view, price, rate in zip(names, images, views, prices, rates):
        item = {
            'name': name.get_text(),
            'image': image.get('src'),
            'view': int(re.sub(pattern, r'\1', view.get_text())),
            'price': float(price.get_text().split('$')[1]),
            'rate': len(rate.select('span.glyphicon-star'))
        }
        items.append(item)
        print(item)

if __name__ == '__main__':
    main()
