from bs4 import BeautifulSoup
import requests
import time

url = 'http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'

#没有做完的失败作业
#商品详情页信息获取
def info(url, data=None):
	wb_data = requests.get(url)
	time.sleep(2)
	soup = BeautifulSoup(wb_data.text, 'lxml')
	titles = soup.select('div.col_sub.mainTitle > h1')
	prices = soup.select('div.su_con > span')
	dates = soup.select('ul.mtit_con_left.fl > li.time')
	areas = soup.select('span.c_25d')
	totalcounts = soup.select('#totalcount')
	categories = soup.select('div.breadCrumb.f12 > span:nth-of-type(3) > a')

	for title, price, date, area, totalcount, category in zip(titles, prices, dates, areas, totalcounts, categories):
		data = {
			'title': title.get_text(),
			'price': price.get_text(),
			'data' : date.get_text(),
			'area' : 'None',
			'totalcount': totalcount.get_text(),
			'category': category.get_text()
			}
		print(data)

    #获取商品详情页url
def start(url):
	wb_data = requests.get(url)
	soup = BeautifulSoup(wb_data.text, 'lxml')
	titles = soup.select('td.t > a.t')
	for title in titles:
		href = title.get('href')
		print(info(href))
start(url)