# ******************** 第一周大作业 ********************
# 爬取 58 同城二手市场-北京-平板电脑这个网页
# http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6
# 这页共 55 个商品, 需要爬取详情页的下列数据
# 包括:
# 1,商品标题 2,浏览量 3,发帖时间 4,价格 5,卖家类型(个人/商家) 6,区域 7,类目

# 查询策略
# 主页列表信息 #infolist
# 商品链接信息 'tr td.img a' #.get('href')
# 1. 商品标题:    (商品页) '.mainTitle h1'
# 2. 浏览量:      (商品页) 'http://jst1.58.com/counter?infoid=%s' % infoid #infoid=商品页链接的[-16,-2]
# 3. 发布日期:    (商品页) '.mtit_con_left.fl .time'
# 4. 价格:       (商品页) '.price.c_f50'
# 5. 卖家类型:    (商品页) '.c_666 .red'  #有文本信息就是商家,否则为个人
# 6. 区域:       (列表页) '.fl .c_666'   #较多商品页中缺失区域信息
# 7. 类目:       (商品页) '.breadCrumb.f12 span:nth-of-type(3) a'

from bs4 import BeautifulSoup
import requests
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
}

def get_soup(url, headers):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    return soup

def get_totalcount(infoid):
    url = 'http://jst1.58.com/counter?infoid=%s' % infoid
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    totalcount = soup.select('p')[0].get_text()[71:]
    return totalcount

def get_area(soup):
    area = ''
    areas = soup.select('.suUl .c_25d a')
    if areas == []:
        area = '无区域信息'
    else:
        for area_info in areas:
            area = area + '-' + area_info.get_text()
        area = area[1:]
    return area

def start_crawl(number_limit):
    page = 0
    number = 0
    while number < number_limit:
        page += 1
        page_url = 'http://bj.58.com/pbdn/pn%s/?PGTID=0d305a36-0000-14c3-b1bb-6944691adca7&ClickID=6' % page
        page_soup = get_soup(page_url, headers)
        urls = page_soup.select('tr td.img a')
        for url in urls:
            url = url.get('href')
            soup = get_soup(url, headers)
            infoid = url[-16:-2]

            data = {
                'title': soup.select('.mainTitle h1')[0].get_text(),
                'totalcount': get_totalcount(infoid),
                'date': soup.select('.mtit_con_left.fl .time')[0].get_text(),
                'price': soup.select('.price.c_f50')[0].get_text(),
                'area': get_area(soup),
                'type': u'商家' if soup.select('p.c_666 .red')[0].get_text(strip=True) != '' else u'个人',
                'category': soup.select('.breadCrumb.f12 span:nth-of-type(3) a')[0].get_text(),
            }

            number += 1
            time.sleep(1)
            print('[%s]:' % number, data)
            if number == number_limit: break
        if len(list(urls)) < 50: break
start_crawl(100)


