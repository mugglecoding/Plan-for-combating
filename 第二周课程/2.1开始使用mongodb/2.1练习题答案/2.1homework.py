from bs4 import BeautifulSoup
import requests
import pymongo

client = pymongo.MongoClient('localhost', 27017)
xiaozhu = client['xiaozhu']  # 建造数据库
sheet_tab = xiaozhu['sheet_tab']  # 建造库中的数据表


def get_imgurl(itemurl):  # 建造进入房子主页获取大图链接的函数
    web_data = requests.get(itemurl)
    soup = BeautifulSoup(web_data.text, 'lxml')
    imgurl = str(soup.select('#curBigImage')[0])
    return (imgurl.split('=')[3].strip('/>'))


def get_sheetdata():  # 从网页获取数据并输入到数据库
    paths = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i)) for i in (range(1, 4))]  # 明确网页路径组
    for path in paths:  # 针对每个路径,获取对应数据

        web_data = requests.get(path)  # 获取网页代码
        soup = BeautifulSoup(web_data.text, 'lxml')  # 用BeautifulSoup,'lxml'方式解析网页代码
        titles = soup.select('#page_list > ul > li > a > img')  # 获取标题
        pics = soup.select('#page_list > ul > li > a')  # 获取图片地址
        adds = soup.select('#page_list > ul > li > div.result_btm_con.lodgeunitname > div > em')  # 获取地址
        prices = soup.select('#page_list > ul > li > div.result_btm_con.lodgeunitname > span.result_price > i')  # 获取价格

        for title, pic, add, price in zip(titles, pics, adds, prices):  # 构造住房信息的单元字典
            data = {
                'title': title.get('title'),
                'pic': get_imgurl(pic.get('href')),
                'add': add.get_text().split('\n')[-1].strip(' '),  # 将信息中的'\n'消除,从列表中地址所在的位置提取地址并消除前后的空格
                'price': int(price.get_text())  # 将字符串转换为整数,以便于之后筛选
            }
            sheet_tab.insert_one(data)  # 将单元字典输入到数据库


get_sheetdata()

for item in sheet_tab.find({'price': {'$gt': 500}}):
    print(item)
