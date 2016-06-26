#!/usr/bin/env python
#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup

# 相对路径,确保index.html和main.py在同一个文件夹
# 相对路径可以方便代码拷贝，移动到其他文件夹不需要修改代码
path = './index.html'

# 使用with open语法打开文件
# 第一个参数是文件地址；第二个参数是文件处理方式：r表示读取文件;w表示写文件
with open(path, 'r') as wb_data:
    content = wb_data.read()

    soup = BeautifulSoup(content, "lxml")
    
    titles = soup.select("body > div > div > div.col-md-9 > div > div > div > div.caption > h4 > a")
    images = soup.select("body > div > div > div.col-md-9 > div > div > div > img")
    reviews = soup.select("body > div > div > div.col-md-9 > div > div > div > div.ratings > p.pull-right")
    prices = soup.select("body > div > div > div.col-md-9 > div > div > div > div.caption > h4.pull-right")
    stars = soup.select("div > div.ratings > p:nth-of-type(2)")

    print(len(titles), len(images), len(reviews), len(prices), len(stars))
    for title, image, review, price, star in zip(titles, images, reviews, prices, stars):
        title_content = title.get_text()
        review_content = review.get_text()
        price_content = price.get_text()
        image_content = image.get("src")
        stars_count = len(star.find_all("span","glyphicon glyphicon-star"))

        data = {
            "title": title_content,
            "review": review_content,
            "image": image_content,
            "price": price_content,
            "star": stars_count
        }

        print(data)

