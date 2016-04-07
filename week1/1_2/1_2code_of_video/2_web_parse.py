#!/usr/bin/env python
#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup


path = './web/new_index.html'

with open(path, 'r') as f:
    soup = BeautifulSoup(f.read(), 'html5lib')
    titles = soup.select('ul > li > div.article-info > h3 > a')
    pics = soup.select('ul > li > img')
    descs = soup.select('ul > li > div.article-info > p.description')
    rates = soup.select('ul > li > div.rate > span')
    cates = soup.select('ul > li > div.article-info > p.meta-info')

    infos = []
    for title, pic, desc, rate, cate in zip(titles, pics, descs, rates, cates):
        info = {
            'title': title.get_text(),
            'pic': pic.get('src'),
            'descs': desc.get_text(),
            'rate': rate.get_text(),
            'cate': list(cate.stripped_strings)
        }
        infos.append(info)

    for i in infos:
        if len(i['rate']) >= 3:
            print(i['title'], i['cate'])
