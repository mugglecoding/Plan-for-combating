# ******************** 2.1 练习作业 ********************
# 爬取小猪短租这个页面的前三页
# http://bj.xiaozhu.com/search-duanzufang-p1-0/
# 把爬取结果存储到 mongo db 数据库中,然后数据库中筛选出所有价格大于等于500元的房源,并打印

from bs4 import BeautifulSoup
import requests
import pymongo
import time

client = pymongo.MongoClient('localhost', 27017)
local_db = client['local_db']
w2_xiaozhu_col = local_db['w2_xiaozhu_col']

headers = {
    'Content-Type': 'text/html; charset=utf-8',
    'User_Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
}
host_url = 'http://bj.xiaozhu.com/'
page_number = 3

def get_soup(url, headers):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    return soup

def get_page_urls(page_number):
    page = 0
    page_limit = page_number
    page_urls = []
    while(page < page_limit):
        page += 1
        page_urls.append(host_url + 'search-duanzufang-p{}-0/'.format(page))
    return page_urls

def get_house_info(url, headers, data=None):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    title       = soup.select('.pho_info h4 em')[0].text
    address     = soup.select('.con_l .pho_info p')[0].get('title')
    price       = soup.select('#pricePart .day_l span')[0].text
    time.sleep(1)
    data = {
        'title':title,
        'address':address,
        'price':int(price),
    }
    return (data)

# print('Testing W2C1.py...')
# page_urls = get_page_urls(page_number)
# for page_url in page_urls:
#     print(page_url)
#     soup = get_soup(page_url, headers)
#     house_list = soup.select('.resule_img_a')
#     for house in house_list:
#         house_url = house.get('href')
#         data = get_house_info(house_url, headers)
#         print(data)
#         w2_xiaozhu_col.insert_one(data)

# print('Testing Database...')
# for doc in w2_xiaozhu_col.find({'price':{'$gte':500}}):
#     print(doc)