from bs4 import BeautifulSoup
import requests

import time


url = 'http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'
web_date = requests.get(url)
soup = BeautifulSoup(web_date.text, 'lxml')
titles = soup.select('td.t > a.t')
times = soup.select('#infolist > table:nth-of-type(5) > tbody > tr.bg > td.t > span.fl')
print(times)
'''标题.浏览量.发帖时间.价格.卖家类型.区域.类目'''