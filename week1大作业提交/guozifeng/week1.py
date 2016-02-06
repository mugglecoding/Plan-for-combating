#coding = utf-8
from bs4 import BeautifulSoup
import requests
import time

#url = 'http://bj.58.com/pingbandiannao/24749763713462x.shtml'

def get_urls(number):
    urls = []
    url = 'http://bj.58.com/pbdn/{}/'.format(str(number))
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    for list_tag in soup.select('a.t'):
        if (url.split('.')[0].strip('http://')) != 'jump':
            urls.append(list_tag.get('href').split('?')[0])
    return urls
def get_page_views(url):#获取浏览量
        id = url.split('/')[-1].strip('x.shtml')
        new_url = 'http://jst1.58.com/counter?infoid={}&userid=&uname=&sid=501342887&lid=1&px=500377157&cfpath=5,38484'.format(str(id))
        wb_data = requests.get(new_url)
        return wb_data.text.split('=')[-1]

def parsing_data(number=0):

    urls = get_urls(number)
    for url in urls:

            wb_data = requests.get(url)
            soup = BeautifulSoup(wb_data.text,'lxml')
            data = {
                '标题':soup.title.text,
                '价格':soup.select('.price')[0].text if soup.find_all('span','price') else None,
                '区域' :list(soup.select('.c_25d')[0].stripped_strings) if soup.find_all('span','c_25d') else None,
                '时间' :soup.select('li.time')[0].text if soup.find_all('li','time') else None,
                '类型' :'个人' if number == 0 else '商家',
                '浏览量':get_page_views(url)
            }
            print(data)
            
parsing_data()
