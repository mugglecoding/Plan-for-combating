from bs4 import BeautifulSoup
import requests
import time
url = 'http://bj.58.com/pingbandiannao/24576277903796x.shtml?psid=143840954190347759329161948&entinfo=24576277903796_0&iuType=p_0&PGTID=0d305a36-0000-1662-1930-4c118dd19cea&ClickID=2'
web_data = requests.get(url)
time.sleep(2)
soup = BeautifulSoup(web_data.text,'lxml')
titles = soup.select(' div.col_sub.mainTitle > h1 ')
timers = soup.select('li.time')
prices = soup.select('div.su_con > span.price.c_f50')
zones = soup.select('div.su_con > span.c_25d')

for title,timer,price,zone in zip(titles,timers,prices,zones):
        data = {
            'title':title.get_text(),
            'timer':timer.get_text(),
            'price':price.get_text(),
            'zone':list(zone.stripped_strings)
        }
        print data
