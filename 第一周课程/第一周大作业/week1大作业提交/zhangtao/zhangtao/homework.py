from bs4 import BeautifulSoup
import requests
import time
urls = []
first_url = 'http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'
web_data = requests.get(first_url)
soup = BeautifulSoup(web_data.text,'lxml')
link_urls = soup.select(' td.t > a.t ')
for i in link_urls:
    urls.append(i.get('href'))
def get_infomation(url):
    data = []
    web_data = requests.get(url)
    soups = BeautifulSoup(web_data.text,'lxml')
    titles = soup.select('div.col_sub.mainTitle > h1')
    timers = soup.select('li.time')
    prices = soup.select('div.su_con > span.price.c_f50')
    zones = soup.select('div.su_con > span.c_25d')
    for title,timer,price,zone in zip(titles,timers,prices,zones):
        single_data = {
            'title':title.get_text(),
            'timer':timers.get_text(),
            'price':price.get_text(),
            'zone':list(zone.stripped_strings)
        }
        data.append(single_data)
    print data
for single_url in urls:
    get_infomation(single_url)



