import time
import requests
from bs4 import BeautifulSoup

'''
应该就在最近，58的代码改了,造成了两个问题：
1. 商品链接不再是明文，而是用了跳转的形式
2. 个人板块中新增了一个叫zhuanzhuan的网站商品内容，详情页和58本身的完全不同。
经观察，寻得解决方案如下：
1. a标签的上一级tr标签中，有一个名为logr的属性，其中包含了商品的id，获得id后便可以合成商品链接。
2. zhuanzhuan商品的tr标签中，不存在logr属性。可以利用if进行筛选。
'''


# get_link_list方法中,seller_type的意义：
# 观察分类url发现，当url为...pbdn/0/时为个人，...pbdn/1/时为商家
# 为了更便捷的获得商品卖家的种类，在获取商品详情页的链接列表时，就依据url进行区分
def get_link_list(seller_type):
    link_list = []
    url = 'http://bj.58.com/pbdn/{}/'.format(str(seller_type))
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    items = soup.select('table tr')
    #之所以不直接爬a标签里的href属性：
    # 58在a标签中使用的是一个跳转链接，如果使用此链接，一方面文本过长，一方面链接中不包含商品ID，便无法配合下面的get_view_num方法获取js地址
    for item in items:
        if item.get('logr') == None:
            None
        else:
            link = 'http://bj.58.com/pingbandiannao/{}x.shtml'.format(str(item.get('logr')).split('_')[3])
            link_list.append(link)
    return link_list


def get_views_num(item_url):
    item_id = item_url.split('/')[-1].strip('x.shtml')
    API = 'http://jst1.58.com/counter?infoid={}'.format(item_id)  # 此为获取浏览量的js地址，与商品ID相关
    js = requests.get(API)
    totalView = js.text.split('=')[-1]  #
    return totalView


def get_items_info(sellerType):
    item_urls = get_link_list(sellerType)
    counter = 1  #计数器
    for item_url in item_urls:

        wb_data = requests.get(item_url)
        soup = BeautifulSoup(wb_data.text,'lxml')

        title = soup.title.text
        price = soup.select('#content span.price')
        area = soup.select('span.c_25d')
        date = soup.select('li.time')
        totalView = get_views_num(item_url)
        # print(title,price,area,date,totalView,sellerType,sep='\n------------\n')

        data = {
            '序号':counter,
            '标题':title,
            '价格':price[0].text,
            '地区':None if area==[] else list(area[0].stripped_strings),  #防止因某些商品没有地区信息而中断
            '日期':date[0].text,
            '浏览量':totalView,
            '卖家类型':'个人' if sellerType == 0 else '商家',
        }

        counter += 1
        print(data)

get_items_info(0)
