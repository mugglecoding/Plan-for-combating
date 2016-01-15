#Author_yaobozhang
from bs4 import BeautifulSoup
import requests

url_host = "http://bj.ganji.com"
url_start = "http://bj.ganji.com/wu"



def get_item_urls(url):
    item_url_lists=[]
    yao_data = requests.get(url)
    yao_data.encoding = 'utf8'
    soup = BeautifulSoup(yao_data.text,'lxml')
    items = soup.select('div.content dt > a')
    for item in items:
        item_url = url_host + item.get('href')
        item_url_lists.append(item_url)
    #print(url_list)
    return item_url_lists

#item_url_lists1=get_item_urls(url_start)
#del item_url_lists1[3]
#print(item_url_lists1)

item_url_lists = ['http://bj.ganji.com/jiaju/', 'http://bj.ganji.com/rirongbaihuo/', 'http://bj.ganji.com/shouji/', 'http://bj.ganji.com/bangong/', 'http://bj.ganji.com/nongyongpin/', 'http://bj.ganji.com/jiadian/', 'http://bj.ganji.com/ershoubijibendiannao/', 'http://bj.ganji.com/ruanjiantushu/', 'http://bj.ganji.com/yingyouyunfu/', 'http://bj.ganji.com/diannao/', 'http://bj.ganji.com/xianzhilipin/', 'http://bj.ganji.com/fushixiaobaxuemao/', 'http://bj.ganji.com/meironghuazhuang/', 'http://bj.ganji.com/shuma/', 'http://bj.ganji.com/laonianyongpin/', 'http://bj.ganji.com/xuniwupin/', 'http://bj.ganji.com/qitawupin/', 'http://bj.ganji.com/ershoufree/', 'http://bj.ganji.com/wupinjiaohuan/']
#spider 1






#get_item_urls(url_start)