from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017)
Ganji = client['Ganji']
url_list = Ganji['url_list']
item_info = Ganji['item_info']


def get_links_from(channel, pages, who_sells='o'):
    list_view = '{}{}{}/'.format(channel, str(who_sells), str(pages))
    wb_data = requests.get(list_view)
    time.sleep(1)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    if soup.find('ul','pageLink'):
        for link in soup.select('.js-item > a'):
            item_link = link.get('href')
            url_list.insert_one({'url': item_link})
            print(item_link)
            # return urls
    else:
        pass # It's the last page !
# for pages in range(1,1000):
#     get_links_from('http://bj.ganji.com/xuniwupin/',pages)


def get_item_info(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    if soup.find('error-tips1'):
        pass
    else:
        title = soup.select('h1.title-name')[0].text
        price = soup.select('i.f22.fc-orange.f-type')[0].text
        date = None if soup.select('i.pr-5')[0].text.split() == [] else soup.select('i.pr-5')[0].text.split()[0]
        area = list(soup.select('div  ul.det-infor li:nth-of-type(3) ')[0].stripped_strings)[1:]
        type = soup.select('#wrapper > div.content.clearfix > div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(1) > span > a')[0].text
        item_info.insert_one({'title': title, 'price': price, 'date': date, 'area': area, 'url': url})
        print({'title': title, 'price': price, 'date':date, 'area': area, 'type':type, 'url': url})

