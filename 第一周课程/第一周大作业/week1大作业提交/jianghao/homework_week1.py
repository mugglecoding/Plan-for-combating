# coding:utf-8
import requests
from bs4 import BeautifulSoup
import time
import re

url = 'http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'
js_url = 'http://jst1.58.com/counter?infoid='+url[95:109]
headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Cookie':'ads_info=t=2015-10-3 10:29:4&p=421&s=1134006,1732074,1551353,1353192,1386250,1506137383,1251113,1300880&y=0|t=2015-10-7 20:21:56&p=740&s=1732074,996961,1219080,996959,1706598&y=0|t=2015-10-9 21:44:45&p=505&s=1689980,1558078,1781257,1134006,1732074,1284444,1358765,1219296,1263688&y=0|t=2015-10-16 12:27:22&p=740&s=1689980,1134006,1732074,1353192,1892017&y=0|t=2015-10-19 15:26:11&p=740&s=1192330,1613266590,996964,1057740,1514794&y=0|t=2015-10-22 19:47:21&p=740&s=1708455005,1645750689,761145,1502891558,836670&y=0|t=2015-10-23 21:40:4&p=740&s=1782097,1645750689,1306139,1781257,1633646027&y=0; unpl=V2_ZzNtbRAFFxxwDkBWch8MDGIGQQpLVhFGdg1AAXwaVANvBBcPclRCFXEURldnGloUZwYZWUJcQRxFCHZRS2lcBGYAEVxDUEYlRQhPZHMpXA1vBhFbQl9HHUU4QWRLKVsAYAYXXENecxRFCQ%3d%3d; mt_subsite=||72%2C1451199098; user-key=8ec81f37-8f17-4d9b-875b-9f59690ca78b; cn=0; __jda=122270672.1994271959.1451199002.1451199002.1451199003.1; __jdv=122270672|click.linktech.cn|t_4_A100220064|cpstopcreothers|cce8477387a844bf80cb247d6297964c; aview=672.1326477|672.1326481|1105.2034900|672.2004304|672.1867740|672.2004285|2694.1389388|672.1544685; ipLocation=%u5317%u4EAC; areaId=1; ipLoc-djd=1-72-2799-0; __jdu=1994271959; aduuid=15d45bb8-737c-407c-a100-62e90d589ed1'
}

def get_urls(url):
	html = requests.get(url,headers=headers)
	soup = BeautifulSoup(html.text,'lxml')
	addrs = soup.select('td.t > a ')
	urls = [addr.get('href') for addr in addrs]
	return urls
def get_msg(url):

	html = requests.get(url,headers=headers)
	soup = BeautifulSoup(html.text,'lxml')
	titles = soup.select('div.col_sub.mainTitle > h1')
	post_times = soup.select('#index_show > ul.mtit_con_left.fl > li.time')
	prices = soup.select('div.su_con > span')
	sellers = soup.select('#tan_tishi > div > div.num_tan_main > div > p > span')
	addrs = soup.select('div.su_con > span > a')
	categories = soup.select('#header > div.breadCrumb.f12 > span > a')
	js_url = 'http://jst1.58.com/counter?infoid='+url[95:109]
	js_html = requests.get(js_url,headers=headers)
	js_soup = BeautifulSoup(js_html.text,'lxml').text
	pattern = re.compile(r'\d+')
	view_counts = re.findall(pattern,js_soup)

	for title,view_count,price,category,post_time,seller,addr in zip(titles,view_counts,prices,categories,post_times,sellers,addrs):
		data = {
			u'标题':title.text,
			u'浏览量':view_counts[4],
			u'价格':price.text,
			u'类目':category.text,
			u'发帖时间':post_time.text,
			u'卖家':u'个人' if len(seller.text)==0 else seller.text,
			u'地址':addr.text
		}
		return data

def action():
	links = get_urls(url)

	for link in links:
		time.sleep(3)
		if len(link)>50:
			msg = get_msg(link)
			with open('D:\homework.txt','a') as file:
				file.write(str(msg)+'\n')
	return file

action()
