# _*_ coding:utf-8 _*_
import io
import sys
from bs4 import BeautifulSoup
import requests
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')     # 改变标准输出的默认编码

# 定义函数，输入主页url,返回值为主页内产品详情链接url列表
def get_webLink(url,main_date=None ):

    global category   # 因手机模式下找不到字段‘北京58同城-北京二手市场-北京二手平板电脑’，因此采用全局变量解决
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
    }
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    titles = soup.select('tr > td.t > a.t')
    category = soup.select('div.nav > a')[2].get_text()      # 通过Selector 选择‘北京58同城-北京二手市场-北京二手平板电脑’，并取list[2]
    # 定义子链接列表 url_link
    url_link = []
    if main_date is None:
        for title in titles:
             url_link.append(title.get('href'))   # 从主页商品列表的主题获得子url
    return url_link

# 定义函数，输入子链接url列表 ,返回值为每个产品的属性字典结构
def get_web(url_link, main_data=None):
    # 通过headers参数设置手机模式，获取产品属性
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4'
    }

    web_data = requests.get(url_link, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    # 通过Selector选择器，获取商品的属性列表
    themes = soup.select('div.left_tit > h1')
    page_times = soup.select('div.attr_other > div.date ')
    # page_views = soup.select('div.attr_other > div > a ')
    product_prices = soup.select('div.good_info > p.attr_price > span.price_now')
    sales_types = soup.select('div.person_detail > a > span.pcate')
    locations = soup.select('div.attr_other > div.location > a ')
    # categorys = soup.select('div.breadCrumb > span.crb_i > a')
    # 测试商品属性列表
    # print(themes, page_times, page_views, product_prices, sales_types, locations, categorys, sep='\n===========================================================\n')
    if main_data is None:
    # 历遍，并将属性编组成字典数据结构
        for theme, page_time, product_price, sales_type, location in zip(themes, page_times, product_prices, sales_types, locations):
            main_data = {
                        '商品标题': theme.get_text(),
                        '发帖时间': page_time.get_text().strip(),
                        '卖家类型': sales_type.get_text(),
                        '商品价格': product_price.get_text(),
                        '区域': location.get_text().strip(),
                        '类目': category
                 }
            print(main_data)

url = 'http://bj.58.com/pbdn/?PGTID=0d305a36-0000-15aa-847c-35bae2e61c0b&ClickID=1'    # url主页地址
# 执行历遍子url的属性索引及打印
for num, url_link in enumerate(get_webLink(url)):
    # print(url_link)         # 测试子链接的列表的输出
    get_web(url_link)
