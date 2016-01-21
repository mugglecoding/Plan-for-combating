from bs4 import BeautifulSoup
import requests
import pymongo
import time

client = pymongo.MongoClient('localhost', 27017)
local_db = client['local_db']
w2_58phnNum_col = local_db['w2_58phnNum_col']

headers = {
    'Content-Type': 'text/html; charset=utf-8',
    'User_Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
}
host_url = 'http://bj.58.com/shoujihao/'

def get_soup(url, headers):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    return soup

# ******************** 2.2.1 练习作业 ********************
# 抓取58同城中的手机号类目下,所有帖子的标题和链接,存储在数据库中.
'''
page = 0
while(True):
    page += 1
    print(page)
    page_url = host_url + 'pn{}/'.format(page)
    soup = get_soup(page_url, headers)
    infos = soup.select('a.t')
    for info in infos:
        data = {
            'title': info.select('strong')[0].text,
            'url': info.get('href').split('?')[0]
        }
        w2_58phnNum_col.insert_one(data)
        print(data)
    time.sleep(1)
    if len(infos) < 30:
        break
'''

# ******************** 2.2.2 练习作业 ********************
# 按照视频中的案例, 把工作流中的爬虫2 设计出来并成功运行后, 储存在数据库中.
# 提示: 从数据库中取出 url 后一次访问页面得到数据并进行存储.
'''
def get_url:
    for doc in local_db.phone_num_58_col.find():
        url = doc['url']
        # ...
        col.insert_one(data)
        # ...
'''