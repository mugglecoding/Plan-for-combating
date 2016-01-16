# -*- coding: utf-8 -*-

import time
import requests
from bs4 import BeautifulSoup

page = 0
limit_count = 300
crawl_list = []
headers = {
    'Content-type': 'text/html;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
}

def parse_info(crawl_url):
    content = requests.get(crawl_url, headers=headers).text
    soup = BeautifulSoup(content, 'lxml')
    title = soup.select('.pho_info h4 em')[0].text
    address = soup.select('.pr5')[0].text.rstrip()
    price = soup.select('.bg_box .day_l span')[0].text.lstrip()
    img_uri = soup.select('#curBigImage')[0].get('src')
    landlord_name = soup.select('.bg_box .lorder_name')[0].text
    landlord_img_uri = soup.select('.bg_box .member_pic img')[0].get('src')
    landlord_role = u'女' if soup.select('.member_girl_ico') else u'男'
    print(u'标题: %s, 地址: %s, 每晚价格: %s, 房屋图片: %s, 房东名字: %s, 房东头像: %s, 房东性别: %s' %
    (title, address, price, img_uri, landlord_name, landlord_img_uri, landlord_role))
    time.sleep(1)

while(len(crawl_list) < limit_count):
    page += 1
    start_url = 'http://bj.xiaozhu.com/search-duanzufang-p%s-0/' % page
    resp = requests.get(start_url, headers=headers)
    content = resp.text
    soup = BeautifulSoup(content, 'lxml')
    info_tags = soup.select('#page_list .pic_list li')
    for info_tag in info_tags:
        href_tag = info_tag.select('.resule_img_a')[0]
        info_url = href_tag.get('href')
        if len(crawl_list) < limit_count:
            crawl_list.append(info_url)
            parse_info(info_url)
        else:
            break