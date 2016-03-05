import requests
from bs4 import BeautifulSoup
import pymongo


client = pymongo.MongoClient('localhost',27017)
xiaozhu = client['xiaozhu']
bnb_info = xiaozhu['bnb_info']

# ====================================================== <<<< 单页行为 >>>> =============================================

url = 'http://bj.xiaozhu.com/search-duanzufang-p20-0/'
wb_data = requests.get(url)
soup = BeautifulSoup(wb_data.text,'lxml')
titles = soup.select('span.result_title')
prices = soup.select('span.result_price > i')

for title, price in zip(titles,prices):
    data = {
        'title':title.get_text(),
        'price':int(price.get_text())
    }
    bnb_info.insert_one(data)
print('Done')

# ====================================================== <<<< 设计函数 >>>> =============================================

def get_page_within(pages):
    for page_num in range(1,pages+1):
        wb_data = requests.get('http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(page_num))
        soup = BeautifulSoup(wb_data.text,'lxml')
        titles = soup.select('span.result_title')
        prices = soup.select('span.result_price > i')
        for title, price in zip(titles,prices):
            data = {
                'title':title.get_text(),
                'price':int(price.get_text())
            }
            bnb_info.insert_one(data)
    print('Done')

# get_page_within(3) 获取前三页面得数据


# 从数据库中进行筛选
# for i in bnb_info.find():
#     if i['price'] >= 500:
#         print(i)