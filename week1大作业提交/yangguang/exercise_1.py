from bs4 import BeautifulSoup
import requests

pages = 1
urls = ['http://bj.58.com/pbdn/pn{}/'.format(str(i)) for i in range(pages)]
ID = 0

def get_ID():
    global ID
    ID += 1
    return ID


def get_seller(sellertag):
    if sellertag == None:
        return('个人')
    else:
        return('商家')


def get_area(alist):
    if  alist == []:
        return('无数据')
    else:
        area_set = []
        for a in alist:
            a = a.get_text()
            area_set.append(a)
        if len(area_set) <= 1:
            return area_set[0]
        else:
            return area_set[0] + '-' + area_set[1]


def get_count(url):
    infoid = url.split('entinfo=')[-1].split('_0')[0]
    db = requests.get('http://jst1.58.com/counter?infoid={}'.format(str(infoid)))

    text = db.text
    items = text.split(';')
    data = {}
    for item in items:
        item = item.split('=')
        data[item[0]]=item[1]

    return(data['Counter58.total'])


def goods_detail(url):
    path = requests.get(url)
    soup = BeautifulSoup(path.text, 'lxml')

    title= soup.select('div.col_sub.mainTitle > h1')[0].get_text()
    count = get_count(url)
    time = soup.select('li.time')[0].get_text()
    price = soup.select('span.price.c_f50')[0].get_text()

    sellers= soup.select('div.wlt_con')
    seller = get_seller(sellers)

    areas = soup.select('span.c_25d > a')
    area = get_area(areas)
    cate = soup.select('span.crb_i')[0].get_text()

    sid = get_ID()

    print('商品编号: '+str(sid))
    print('商品类目: '+str(cate))
    print('商品标题: '+str(title))
    print('商品价格: '+str(price))
    print('浏览次数: '+str(count))
    print('卖家区域: '+str(area))
    print('卖家类型: '+str(seller))
    print('发帖时间: '+str(time))
    print('------------------------------\n')


def py58(url):
    db = requests.get(url)
    soup = BeautifulSoup(db.text, 'lxml')
    details = soup.select('td.t > a.t')
    for detail in details:
        detail = detail.get('href')
        goods_detail(detail)


for url in urls:
    py58(url)

print('\n*****************************************\n********    Mission Complete!    ********\n*****************************************\n')
