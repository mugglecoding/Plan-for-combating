from bs4 import BeautifulSoup
import requests
import time

url = 'http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'


def get_info(url, data=None):
    wb_data = requests.get(url).text
    soup = BeautifulSoup(wb_data, 'lxml')
    title = soup.select('div.col_sub.mainTitle > h1')[0].get_text()
    date = soup.select('ul.mtit_con_left.fl > li.time')[0].get_text()
    price = soup.select('div.su_con > span.price')[0].get_text()
    seller_type = u'商家' if soup.select('div > header > h3 > span') else u'个人'
    if len(soup.select('div.su_con > span > a')) == 2:
        district = str(soup.select('div.su_con > span > a')[0].get_text())+str(soup.select('div.su_con > span > a')[1].get_text())
    elif len(soup.select('div.su_con > span > a')) == 1:
        district = soup.select('div.su_con > span > a')[0].get_text()
    else:
        district = None
    cate = soup.select('div.breadCrumb.f12 > span > a')[2].get_text()
    if data == None:
        data = {
            'title':title,
            'date':date,
            'price':price,
            'seller_type':seller_type,
            'district':district,
            'cate':cate
        }
        print(data)


def more_pages(url):
    wb_data = requests.get(url).text
    soup = BeautifulSoup(wb_data, 'lxml')
    links = soup.select('td.t > a.t')
    for link in links:
        info_url = link.get('href')
        get_info(info_url)
        time.sleep(2)

more_pages(url)