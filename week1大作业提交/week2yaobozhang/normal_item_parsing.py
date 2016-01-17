#Author_yaobozhang
from bs4 import BeautifulSoup
import requests
import time
import pymongo


client = pymongo.MongoClient('localhost',27017)
ceshi  = client['ceshi']
url_list = ceshi['url_list3']
item_info = ceshi['item_info3']

def get_links_from(channel,pages,who_sells=''):
    list_view = '{}{}o{}/'.format(channel,who_sells,str(pages))
    yao_data = requests.get(list_view)
    yao_data.encoding = 'utf8'
    time.sleep(3)
    soup = BeautifulSoup(yao_data.text,'lxml')
    #Exist_page = soup.find('html',lang='zh').get('data-gjch')
    Exist_page = soup.select('html[lang="zh"]')[0].get('data-gjch')
    print('test',Exist_page)
    index = Exist_page.index("pn=")+3
    Exist_flag = (pages == int(Exist_page[index]))
    if Exist_flag:
        for link in soup.select('dd.feature a.ft-tit'):
            item_link = link.get('href')
            url_list.insert_one({'url':item_link})
            get_item_info(item_link,pages,who_sells)
            print(item_link)
    else:
        pass

#get_links_from('http://bj.ganji.com/yingyouyunfu/',21)
#url_list.remove()

#soider 2

def get_item_info(url,pages,who_sells):
    yao_data = requests.get(url)
    soup = BeautifulSoup(yao_data.text,'lxml')
    titles = soup.select('.title-name')
    dates = soup.select('i.pr-5')
    prices = soup.select('i.f22')
    areas = soup.select('ul.det-infor > li > a')
    categorys = soup.select('ul.det-infor > li > span > a')
    area_start = []
    category_start = []
    #categorys = list(categorys[0].stripped_strings)
    for title,date,price,area,category in zip(titles,dates,prices,areas,categorys):
        data = {
         'title':title,
         'price':price.get_text(),
         'date':date.get_text(),
         'area':area_start.append(list(area.stripped_strings)),
         'category': category_start.append(list(category.stripped_strings)),
         'cate':'个人' if who_sells == '' else '商家'
        }
    del data['area'][0]
    item_info.insert_one(data)
