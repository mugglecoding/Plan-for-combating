from bs4 import BeautifulSoup
import requests
import time
import re

headers = {
    'Content-type': 'text/html;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari'
                  '/537.36'

}
mobieheaders = {
    'Content-type': 'text/html;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4'
}
def get_count_url(product_url):

    id = 'http://jst1.58.com/counter?infoid='
    infoid = re.findall(r"info=(.+?)_0", product_url)

    id = id + infoid[0]



    totalcount = requests.get(id, headers=mobieheaders)
    response = totalcount.content.decode('utf-8')
    pattern = re.compile(r'\d+')
    result = re.findall(pattern, response)
    product_view_count = result[4]
    time.sleep(1)
    return product_view_count




def parse_info(product_url):
    product_area_list = []
    web_data = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    product_title = soup.select('div.col_sub.mainTitle h1')[0].text
    product_publish_time = soup.select('ul.mtit_con_left.fl li.time')[0].text
    product_price = price = soup.select('span.price.c_f50')[0].text
    areas = soup.select('div.col_sub.sumary ul.suUl a')
    product_view_count = soup.select('ul.mtit_con_left.fl li.count')[0].text
    for i in areas:
        product_area_list.append(i.text)
    # product_area_list.remove('')
    product_type = soup.select('header div.breadCrumb.f12 a')[2].text.lstrip()
    user_type = soup.select('body div.num_tan div.num_tan_in div.num_tan_main div.num_tan_text span')[2].text
    if '商家' in user_type:
        user = '商家'
    else:
        user = '个人'
        ###############################################
        #get_count_url()通过js访问获得浏览量，目前有bug,因周一有考试,实在没时间再调试了
        #product_view_count = get_count_url(product_url)
        ###############################################

    print(u'商品标题: %s,浏览量: %s, 发帖时间: %s, 价格: %s, 卖家类型: %s, 区域 : %s, 类目: %s' % (
        product_title, product_view_count, product_publish_time, product_price, user, product_area_list,
        product_type))
    time.sleep(1)
    return


url = 'http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6&selpic=2'
page = 1

web_data = requests.get(url, headers=headers)

soup = BeautifulSoup(web_data.text, 'lxml')
url_list = soup.select('td.img a')

for url in url_list:
    print('Page ' + str(page) + ': ')
    web_site = url.get('href')
    parse_info(web_site)
    page += 1


