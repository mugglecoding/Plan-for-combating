#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

# 性别不同，标签的class属性内容不同，通过这个差异区分房东性别
def get_lorder_sex(class_name):
    if class_name == ['member_boy_ico']:
        return '男'
    elif class_name == ['member_girl_ico']:
        return '女'

def get_links(url):
    wb_data = requests.get(url)

    # 开始解析网页数据
    soup = BeautifulSoup(wb_data.text, 'lxml')

    # 鼠标放到图片上，右键，审查元素，找到链接的css selector
    links = soup.select("#page_list > ul > li > a")   

    #  由于链接有好多个，soup.select返回的是列表，需要用for一个个取出来
    for link in links:
        # 由于链接地址在标签的href属性里面，所以要用get获取
        href = link.get("href")

        # 把得到的详情页链接，传给函数，这个函数可以得到详细数据
        get_detail_info(href)    

def get_detail_info(url):
    wb_data = requests.get(url)

    # 开始解析详情页数据
    soup = BeautifulSoup(wb_data.text, 'lxml')

    # 获取名称
    titles = soup.select("body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > h4 > em")

    # 获取地址
    addresss = soup.select("body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > p > span.pr5")

    # 获取价格
    prices = soup.select("#pricePart > div.day_l > span")

    # 获取图片
    images = soup.select("#curBigImage")

    # 获取房东头像
    avartars = soup.select("#floatRightBox > div.js_box.clearfix > div.member_pic > a > img")

    # 获取房东姓名
    names = soup.select("#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a")

    # 获取房东性别
    sexs = soup.select("#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > span")

    for title, address, price, image, avartar, name, sex in zip(titles, addresss, prices, images, avartars, names, sexs):
        # 从标签里面提取内容
        data = {
            "title": title.get_text(),
            "address": address.get_text(),
            "price": price.get_text(),
            "image": image.get("src"),
            "avartar": avartar.get("src"),
            "name": name.get_text(),
            "sex": get_lorder_sex(sex.get("class"))
        }
        print(data)

# 生成10个列表页面地址
urls = ["http://bj.xiaozhu.com/search-duanzufang-p{}-0/".format(number) for number in range(1, 10)]

# 从链接列表中，用for一个个取出来
for single_url in urls:
    # 把得到的列表页面链接，传给函数，这个函数可以得到详情页链接
    get_links(single_url)

