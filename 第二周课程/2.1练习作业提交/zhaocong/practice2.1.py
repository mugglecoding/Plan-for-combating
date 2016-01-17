from bs4 import BeautifulSoup
import requests
import time
import pymongo

page = 1

client = pymongo.MongoClient('localhost',27017)
rent_data = client['rent_data']
selected_sheet = rent_data['selected_sheet']
def parse_info(search_url):  # 定义爬去网页信息函数
    web_site = requests.get(search_url)

    soup = BeautifulSoup(web_site.text, 'lxml')

    titles = soup.select(' #page_list .pic_list .result_intro a')  # 获取标题列表

    info_urls = soup.select(' #page_list .pic_list li .resule_img_a')  # 获取租房链接列表

    prices = soup.select(' #page_list .pic_list .result_price i')  # 获取价格列表

    for title, info_url, price in zip(titles, info_urls, prices):  # 循环将title,url,price写入data字典中
        data = {
            'title': title.text,
            'url': info_url.get('href'),
            'price':int(price.text) #提前转换为int类型,方面后面筛选
        }
        selected_sheet.insert_one(data)


    time.sleep(1)


while (page < 4):
    url = 'http://bj.xiaozhu.com/search-duanzufang-p%s-0/' % page

    parse_info(url)

    page += 1
#$lt/$lte/$gt/$gte/$ne,依次等价于< ,<= ,> , >= , !=
for item in selected_sheet.find({'price':{'$gte':500}}):
    print(item)

