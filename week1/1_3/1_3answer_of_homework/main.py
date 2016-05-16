#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

# 根据结果观察不同性别会用不同的图标样式（class），设计一个函数进行转换
def get_lorder_sex(class_name):
    if class_name == 'member_girl_ico':
        return u'女'

    return u'男'

def get_fangzi_info(url):
    r = requests.get(url)

    # 检查网页是否存在，存在则状态码为200
    if r.status_code != 200:
        return

    # 这里采用html.parser引擎，因为lxml和html5lib引擎在这里解析有问题
    soup = BeautifulSoup(r.text, 'html.parser')

    # 获取匹配的标签
    title_tags = soup.select("body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > h4 > em")
    address_tags = soup.select("body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > p > span.pr5")
    price_tags = soup.select("#pricePart > div.day_l > span")
    image_tags = soup.select("#curBigImage")
    lorder_avartar_tags = soup.select("#floatRightBox > div.js_box.clearfix > div.member_pic > a > img")
    lorder_name_tags = soup.select("#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a")
    lorder_sex_tags = soup.select("#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > span")

    # 分析网页，一个页面只有一个符合条件的标签，所以取第一个标签
    # 如果不做判断，直接取，部分网页会报错
    title_tag = title_tags[0] if len(title_tags) > 0 else ""
    address_tag = address_tags[0] if len(address_tags) > 0 else ""
    price_tag = price_tags[0] if len(price_tags) > 0 else ""
    image_tag = image_tags[0] if len(image_tags) > 0 else ""
    lorder_avartar_tag = lorder_avartar_tags[0] if len(lorder_avartar_tags) > 0 else ""
    lorder_name_tag = lorder_name_tags[0] if len(lorder_name_tags) > 0 else ""
    lorder_sex_tag = lorder_sex_tags[0] if len(lorder_sex_tags) > 0 else ""

    # 从标签里面提取内容
    data = {
    	"title": title_tag.get_text(),
    	"address": address_tag.get_text(),
    	"price": price_tag.get_text(),
    	"image": image_tag.get("src"),
    	"lorder_avartar": lorder_avartar_tag.get("src"),
    	"lorder_name": lorder_name_tag.get_text(),
    	"lorder_sex": get_lorder_sex(lorder_sex_tag.get("class"))
    }
    print(data)


for number in range(1, 301):
    list_index_url = "http://bj.xiaozhu.com/search-duanzufang-p{}-0/".format(number)

    r = requests.get(list_index_url)

    # 检查网页是否存在，存在则状态码为200, 不存在则跳过
    if r.status_code != 200:
        continue

    # 从列表页面提取详细信息的链接
    soup = BeautifulSoup(r.text, 'html.parser')
    divs = soup.select("#page_list > ul > li > div.result_btm_con.lodgeunitname")    
    for div in divs:
        url = div.get("detailurl")
        get_fangzi_info(url)
