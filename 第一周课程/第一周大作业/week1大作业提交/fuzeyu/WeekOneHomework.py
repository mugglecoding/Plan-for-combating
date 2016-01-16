from bs4 import BeautifulSoup
import requests
import time


url = 'http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'

page  = requests.get(url)
soup2 = BeautifulSoup(page.text,'lxml')
webs = soup2.select('td.t > a.t')
url_list = [web.get('href') for web in webs]

def content(url):
    time.sleep(1)
    page2 = requests.get(url)
    soup = BeautifulSoup(page2.text,'lxml')
    titles = soup.select('h1')
    dates = soup.select('ul.mtit_con_left.fl > li.time')
    prices = soup.select('#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li:nth-of-type(1) > div.su_con > span')
    cates = soup.select('#header > div.breadCrumb.f12 > span:nth-of-type(3) > a')
    for title,date,price,cate in zip(titles,dates,prices,cates):
        data ={
            '商品标题': title.get_text(),
            '发布日期': date.get_text(),
            '价格':price.get_text(),
            '类目':cate.get_text()
        }
        print (data)

for url in url_list:
    content(url)

