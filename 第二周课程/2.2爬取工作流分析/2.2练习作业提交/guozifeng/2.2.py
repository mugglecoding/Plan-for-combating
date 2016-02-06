from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost',27017)
_58shouji = client['_58shouji']
url_list = _58shouji['url_list']
pages = 0
while True:
    pages += 1
    url = 'http://bj.58.com/shoujihao/pn%s/' % str(pages)
    time.sleep(1)
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    if soup.find('a','t'):
        infos =soup.select('a.t')
        for info in infos:
            data = {
                'url':info.get('href'),
                #'price':info.select('.price')[0].text if info.find_all('b','price') else u'面议',
                'title':info.select('strong')[0].get_text()
            }
            url_list.insert_one(data)
            print(data)
    else:
        break
    
