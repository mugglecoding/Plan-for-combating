#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import pymongo
import requests
from bs4 import BeautifulSoup

# 连接MongoDB，数据库地址为:localhost。端口号为: 27017
# 注意MoongoClient大小写，不要写成mongoclient
client = pymongo.MongoClient('localhost', 27017)

# 从MongoDB中选择名称为 tongcheng 的数据库
tongcheng = client['tongcheng']

# 从 tongcheng 数据库选择名称为 shoujihao 的表
# 存储列表详情页面链接
shoujihao = tongcheng['shoujihao']

# 从 tongcheng 数据库选择名称为 infos 的表
# 存储详情页面的手机号信息
infos = tongcheng['infos']


# spider1
def get_links_from(page):
	# 根据列表页面链接规律，拼接列表页面地址
    url = 'http://bj.58.com/shoujihao/pn{}/'.format(page)

    # 请求列表页面地址
    wb_data = requests.get(url)

    # 延时一秒钟，太快容易被封IP
    time.sleep(1)

    # 开始解析网页数据
    soup = BeautifulSoup(wb_data.text, 'lxml')

    # 鼠标放到每个小方格的手机号上，右键，审查元素，再右键，提取Css Path
    titles = soup.select('#infolist > div > ul > div > ul > li > a.t > strong')

    # 鼠标再放到链接的标签上，右键，提取Css Path
    links = soup.select('#infolist > div > ul > div > ul > li > a.t')

    # 由于soup.select得到的是列表，需要用for一个个遍历出来
    for title, link in zip(titles, links):
        data = {
	        # 由于标题的文本内容在<strong></strong>标签之间，用get_text()提取
            'title': title.get_text(),

            # 由于链接地址在标签的href属性里面，所以用get提取
            'url': link.get('href')
        }

        print(data)

        # 插入数据库，注意不要搞混shoujihao和infos数据库
        shoujihao.insert_one(data)

# spider2
def get_item_info(url):
	# 请求详情页面地址
    wb_data = requests.get(url)

    # 延时一秒钟，太快容易被封IP
    time.sleep(1)

    # 开始解析网页数据
    soup = BeautifulSoup(wb_data.text, 'lxml')	

    # 鼠标放到标题上，右键，审查元素，再右键，提取Css Path
    titles = soup.select('#main > div.col.detailPrimary.mb15 > div.col_sub.mainTitle > h1')

    # 鼠标放到价格信息上，右键，审查元素，再右键，提取Css Path
    prices = soup.select('#main > div.col.detailPrimary.mb15 > div.col_sub.sumary > ul > li > div.su_con > span')

    # 由于soup.select得到的是列表，需要用for一个个遍历出来
    for title, price in zip(titles, prices):
    	# 由于标题的文本内容在<h1></h1>标签之间，用get_text()提取
    	title_text = title.get_text()

    	# 由于价格的文本内容在<span></span>标签之间，用get_text()提取
    	price_text = price.get_text()

    	data = {
    		"url": url,
    		# 提取的内容有很多空白字符，需要replace替换掉
    		"title": title_text.replace("\n", "").replace("\t", "").replace(" ", ""),
    		"price": price_text.replace("\n", "").replace("\t", "").replace(" ", "")
    	}

    	print(data)

    	# 插入数据库，注意不要搞混shoujihao和infos数据库
    	infos.insert(data)

# 获取多个列表页面内的详情页面链接，插入数据库
for page in range(1, 1000):
	get_links_from(page)

# 获取列表页面得到的详情页面链接，需要从数据库读取
for info in shoujihao.find():
	url = info["url"]

	get_item_info(url)

