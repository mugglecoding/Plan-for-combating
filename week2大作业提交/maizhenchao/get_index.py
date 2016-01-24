from bs4 import BeautifulSoup
import requests

start_url = 'http://bj.ganji.com/wu/'
url_host = 'http://bj.ganji.com'

def get_index(url):
    channel_list = []
    web = requests.get(url)
    soup = BeautifulSoup(web.text, 'lxml')
    indices = soup.select('dl.fenlei > dt > a')
    for index in indices:
        channel_url =url_host + index.get('href')
        channel_web = requests.get(channel_url)
        channel_soup = BeautifulSoup(channel_web.text, 'lxml')
        ischannel_link = channel_soup.find('li', class_='js-item')
        if ischannel_link:
            channel_list.append(channel_url)
    return channel_list

channel_list = get_index(start_url)
