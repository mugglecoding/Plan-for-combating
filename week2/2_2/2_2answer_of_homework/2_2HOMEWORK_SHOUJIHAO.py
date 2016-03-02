import requests
from bs4 import BeautifulSoup
import pymongo


client = pymongo.MongoClient('localhost',27017)
tongcheng_info = client['tongcheng_info']
shoujihao = tongcheng_info['shoujihao']

# ====================================================== <<<< 单页行为 >>>> =============================================
url = 'http://bj.58.com/shoujihao/'
wb_data = requests.get(url)
soup = BeautifulSoup(wb_data.text,'lxml')
numbers = soup.select('strong.number')
prices = soup.select('b.price')
links = soup.select('a.t')

for number, price, link in zip(numbers,prices,links):
    data = {
        'title':number.get_text(),
        'price':price.get_text(),
        'link' :link.get('href')
    }
    shoujihao.insert_one(data)
print('Done')

# ====================================================== <<<< 设计函数 >>>> =============================================
def get_pages_within(pages):
    for page_num in range(1,pages+1):
        wb_data = requests.get('http://bj.58.com/shoujihao/pn{}/'.format(page_num))
        soup = BeautifulSoup(wb_data.text,'lxml')
        numbers = soup.select('strong.number')
        prices = soup.select('b.price')
        links = soup.select('a.t')

        for number, price, link in zip(numbers,prices,links):
            data = {
                'title':number.get_text(),
                'price':price.get_text(),
                'link' :link.get('href')
            }
            shoujihao.insert_one(data)
        print('Done')

