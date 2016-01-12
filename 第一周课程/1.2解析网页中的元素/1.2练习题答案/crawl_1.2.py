# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

# 这里写本地的目录
file_path = '/Users/apple/Documents/1.2练习作业补充材料/index.html'
soup = BeautifulSoup(open(file_path), 'lxml')
product_tags = soup.select('.container .thumbnail')
for product_tag in product_tags:
    product_name_tag = product_tag.select('.caption h4 a')[0]
    product_name = product_name_tag.text
    product_price_tag = product_tag.select('.caption .pull-right')[0]
    product_price = product_price_tag.text
    views_count_tag = product_tag.select('.ratings .pull-right')[0]
    views_count = views_count_tag.text.split(' ')[0]
    img_tag = product_tag.select('img')[0]
    img_url = img_tag.get('src')
    grade_tags = product_tag.select('.glyphicon-star')
    grade = '%s颗星' % len(grade_tags)
    print(u'商品标题: %s, 商品价格: %s, 浏览量: %s, 图片地址: %s, 评分: %s' %
        (product_name, product_price, views_count, img_url, grade))