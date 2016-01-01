#encoding:utf-8
from bs4 import BeautifulSoup
import requests

index_url = 'http://bj.ganji.com/wu/'
prefix_url = 'http://bj.ganji.com'

def get_channel_urls(url):
    req_content = requests.get(url)
    soup = BeautifulSoup(req_content.text,'lxml')
    urls = soup.select('dl.fenlei > dt > a')
    for item in urls:
        page_url = prefix_url + item.get('href')
        print(page_url)

# get_channel_urls(index_url)

channel_urls = '''
    http://bj.ganji.com/jiaju/
    http://bj.ganji.com/rirongbaihuo/
    http://bj.ganji.com/shouji/
    http://bj.ganji.com/bangong/
    http://bj.ganji.com/nongyongpin/
    http://bj.ganji.com/jiadian/
    http://bj.ganji.com/ershoubijibendiannao/
    http://bj.ganji.com/ruanjiantushu/
    http://bj.ganji.com/yingyouyunfu/
    http://bj.ganji.com/diannao/
    http://bj.ganji.com/xianzhilipin/
    http://bj.ganji.com/fushixiaobaxuemao/
    http://bj.ganji.com/meironghuazhuang/
    http://bj.ganji.com/shuma/
    http://bj.ganji.com/laonianyongpin/
    http://bj.ganji.com/xuniwupin/
    http://bj.ganji.com/qitawupin/
    http://bj.ganji.com/ershoufree/
    http://bj.ganji.com/wupinjiaohuan/
'''