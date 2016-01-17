# ******************** 2.4 练习作业 ********************
# 爬取赶集网-北京-二手市场的所有类目的商品信息,
# http://bj.ganji.com/wu/
# 所有加粗类目,一共能看到20个左右
# 二手家具, 家居百货, 二手手机, 手机号码, 设备/办公用品, 农产品......
# 建议 个人 / 商家 分开爬取
# 需要信息: 商品标题, 发帖时间, 价格, 交易地点, 类型, 卖家类型(个人/商家)
# 也就是说,赶集网-北京-二手市场的所有帖子都需要爬取,除了某些不规则的页面可以不包括在内.
# 建议使用多进程的方式爬取.

from multiprocessing import Pool
from bs4 import BeautifulSoup
import requests
import pymongo

client   = pymongo.MongoClient('localhost', 27017)
local_db = client['local_db']
w2_itmUrl_col   = local_db['w2_itmUrl_col']
w2_itmInfo_col  = local_db['w2_itmInfo_col']

headers = {
    'Content-Type': 'text/html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Cookie': 'citydomain=bj; ganji_xuuid=eea59d9c-8b6b-4197-8bcb-e18db2236213.1452772376566; ganji_uuid=2488988877099655998455; GANJISESSID=4bcb39256320bd9d69cf4010fe25cf66; hotPriceTip=1; __utma=32156897.262518560.1452570775.1452790802.1452881661.4; __utmb=32156897.11.10.1452881661; __utmc=32156897; __utmz=32156897.1452790802.3.2.utmcsr=bj.ganji.com|utmccn=(referral)|utmcmd=referral|utmcct=/wu/; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A71596067824%7D',
}

def get_soup(url, headers):
    wb_data = requests.get(url, headers=headers)
    wb_data.encoding = 'utf-8'                    # 出现乱码时可以采用此行语句
    soup = BeautifulSoup(wb_data.text, 'lxml')
    return soup

def get_place(soup):
    place = ''
    places = soup.select('div.leftBox > div > div > ul > li > a')
    if not places:
        place = None
    else:
        for place_info in places:
            place += '-' + place_info.text
        place = place[1:]
    return place

def get_itmInfo():
    for doc in w2_itmUrl_col.find({'itm_st': False}):
        print(doc)
        soup = get_soup(doc['url'], headers)
        data = {
            'title': soup.select('h1.title-name')[0].text,
            'time' : soup.select('i.pr-5')[0].get_text(strip=True),
            'price': soup.select('i.f22')[0].text,
            'place': get_place(soup),
            'item_type': soup.select('div.leftBox > div > div > ul > li > span > a')[0].text,
            'who_sells': doc['who_sells'],
        }
        w2_itmInfo_col.insert_one(data)
        doc.update({'itm_st': True})
        w2_itmUrl_col.update({'_id': doc['_id']}, doc)
    print('Done crawling some items...')

if __name__ == '__main__':
    print('Week2 Project...')
    pool = Pool()
    col = w2_itmUrl_col.find({'itm_st': False})
    while col.count() != 0:
        get_itmInfo()
        col = w2_itmUrl_col.find({'itm_st': False})

