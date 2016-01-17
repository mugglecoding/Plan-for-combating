#coding=utf-8
from bs4 import BeautifulSoup
import requests
import time
import pymongo
from channel_extact  import channel_list

client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
tab_url_list = ganji['url_list']
tab_item_info = ganji['item_info']

# headers = {
#     'Host': '3g.ganji.com',''
#     'Upgrade-Insecure-Requests':'1',
#     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4',
# }



def get_item_info(url,puid):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    title_exist = soup.select('h1.title-name')
    if title_exist == None or title_exist==[]:
         pass
    else:
        puid = puid
        title = title_exist[0].text.strip()
        time = soup.select('li > i.pr-5')[0].text.strip()
        itype = soup.select('ul.det-infor > li > span > a')[0].text.strip()
        price = soup.select('i.f22.fc-orange.f-type')[0].text.strip()
        sellers = soup.select('ul.det-infor > li > span.fc-orange')
        if sellers == '[商家]' :
            seller = '商家'
        else:
            seller = '个人'

        def get_area(alist):
            if  alist == [] or alist == None:
                return('无数据')
            else:
                area_set = []
                area = ''
                for a in alist:
                    a = a.get_text().strip()
                    area_set.append(a)
                for i in range(len(area_set)):
                    area = area + area_set[i] + " - "
                return area.rstrip(" - ")
        area_pre = soup.find(attrs={'class':'p-z-type'})

        if area_pre == [] or area_pre == None:
            areas = soup.select('ul.det-infor > li > a')
        else :
            areas = area_pre.find_parent().find_next_sibling().find_all(target='_blank')
        area = get_area(areas)

        # print(title,'\n')
        # print(time,'\n')
        # print(itype,'\n')
        # print(price,'\n')
        #print(area)
        # print(get_area(areas))

        item_data = {
            'puid' : puid,
            'title' : title,
            'time' : time,
            'type' : itype,
            'price': price,
            'seller': seller,
            'area': area,
        }
        tab_item_info.update(item_data,{'$set':{'puid':puid}},upsert=True)


def get_links_from(channel, pages, who_sells='a3'):
    list_view = '{}/{}o{}/'.format(channel, str(who_sells), str(pages))
    wb_data = requests.get(list_view)
    time.sleep(3)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    pagebox = soup.select('div.pageBox')
    puids = soup.select('li.js-item')

    if pagebox == None or pagebox ==[] or puids==[] or puids == None:
        pass
    else:
        #links = soup.select('ul > li > a.ft-tit')
        # return urls
        for puid in puids:
            puid = puid.get('data-puid')
            url = channel+puid+'x.htm'
            get_item_info(url,puid)

            data = {
                'url' : url,
                'puid' : puid
            }
            tab_url_list.update(data,{'$set':{'puid': puid}},upsert=True)
            print(puid)
#get_links_from('http://bj.ganji.com/shouji/',3)