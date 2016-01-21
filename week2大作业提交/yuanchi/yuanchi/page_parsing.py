from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost',27017)
ceshi = client['ceshi']
url_list = ceshi['url_list3']
item_info = ceshi['item_info']
headers = {
    'User-Agent':'User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'
}

#spider 1

#通过who_sells出现推广的问题，故直接通过商家特性来判断是个人还是商家
def get_links_from(channel,pages):
    #http://bj.ganji.com/jiaju/a3o11/
    #ttp://bj.ganji.com/wupinjiaohuan/o3/#两种不同url
    if channel in ['http://bj.ganji.com/xuniwupin/','http://bj.ganji.com/qitawupin/','http://bj.ganji.com/ershoufree/','http://bj.ganji.com/wupinjiaohuan/']:
        list_view = '{}o{}/'.format(channel,str(pages))
        wb_data = requests.get(list_view,headers=headers)
        #time.sleep(1)
        soup = BeautifulSoup(wb_data.text,'lxml')
        if soup.find('ul','pageLink clearfix'):
            for link in soup.select('#wrapper > div.leftBox > div.layoutlist > dl > dt > div > a'):
                item_link = link.get('href')
                url_list.insert_one({'url':item_link})
                print(item_link)

        else:
            #pass
            print('重复页面')
    else:
        list_view = '{}a3o{}/'.format(channel,str(pages))
        wb_data = requests.get(list_view,headers=headers)
        #time.sleep(1)
        soup = BeautifulSoup(wb_data.text,'lxml')
        if soup.find('ul','pageLink clearfix'):
            for link in soup.select('#wrapper > div.leftBox > div.layoutlist > dl > dd.feature > div > ul > li > a'):
                item_link = link.get('href')
                url_list.insert_one({'url':item_link})
                print(item_link)

        else:
            #pass
            print('重复页面')


def get_item_info(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    print(url)#追踪出错url
    if soup.find_all(src=" http://sta.ganjistatic1.com/src/image/v5/expire.png"):#物品已售出，信息过期，如http://bj.ganji.com/shouji/1303939091x.htm
        print('信息已过期')
    else:
        if soup.select('div.error'):#错误界面
            pass
        else:
            if soup.select('h1.title-name'):#会出现此类界面，判断后跳过：http://bj.ganji.com/ershoubijibendiannao/386647282x.htm
                title = soup.select('h1.title-name')[0].text
                #title = soup.title.text
                time = soup.select('i.pr-5')[0].text.strip().split('发布')[0]
                type = soup.select('ul.det-infor > li > span > a')[0].text
                price = soup.select('i.f22.fc-orange.f-type')[-1].text if soup.find_all('i','f22 fc-orange f-type') else None
                area_list = soup.select('div.leftBox > div > div > ul > li')[9]
                area = ''.join(list(area_list.stripped_strings))
                seller = soup.select('span.fc-orange')[0].text
                if seller == '':
                    seller = '个人'
                else:
                    seller = '商家'
                item_info.insert_one({'title':title,'time':time,'type':type,'price':price,'area':area,'seller':seller})
                print({'title':title,'time':time,'type':type,'price':price,'area':area,'seller':seller})
            else:
                print('特殊页面')


get_item_info('http://bj.ganji.com/shouji/1303939091x.htm')

#get_links_from('http://bj.ganji.com/ershoufree/',2)