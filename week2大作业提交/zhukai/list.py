from bs4 import BeautifulSoup
import requests

url_host = 'http://bj.ganji.com/wu'
start_url = 'http://bj.ganji.com/wu'


def get_channel_urls(url):
    wb_data = requests.get(start_url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    links = soup.select('dl.fenlei dt a')
    for link in links:
        page_url = url_host + link.get('href')
        print(page_url)


get_channel_urls(start_url)

channel_list = '''
http://bj.ganji.com/wu/jiaju/
http://bj.ganji.com/wu/rirongbaihuo/
http://bj.ganji.com/wu/shouji/
http://bj.ganji.com/wu/shoujihaoma/
http://bj.ganji.com/wu/bangong/
http://bj.ganji.com/wu/nongyongpin/
http://bj.ganji.com/wu/jiadian/
http://bj.ganji.com/wu/ershoubijibendiannao/
http://bj.ganji.com/wu/ruanjiantushu/
http://bj.ganji.com/wu/yingyouyunfu/
http://bj.ganji.com/wu/diannao/
http://bj.ganji.com/wu/xianzhilipin/
http://bj.ganji.com/wu/fushixiaobaxuemao/
http://bj.ganji.com/wu/meironghuazhuang/
http://bj.ganji.com/wu/shuma/
http://bj.ganji.com/wu/laonianyongpin/
http://bj.ganji.com/wu/xuniwupin/
http://bj.ganji.com/wu/qitawupin/
http://bj.ganji.com/wu/ershoufree/
http://bj.ganji.com/wu/wupinjiaohuan/
'''