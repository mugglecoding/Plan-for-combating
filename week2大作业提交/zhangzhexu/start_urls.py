# coding=gbk
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

from bs4 import BeautifulSoup
import requests

url_host = 'http://bj.ganji.com'
start_url = 'http://bj.ganji.com/wu/'

def get_classes(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    types = soup.select('dl.fenlei > dt > a')
    urls =[]
    for type in types:
        type_url =url_host + type.get('href')
        print(type_url)
    urls.append(type_url)

    return(type_url)

#type_urls =get_classes(start_url)
