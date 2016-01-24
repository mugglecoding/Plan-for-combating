# __author__ = 'xjlin'
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests

start_url = 'http://bj.ganji.com/wu/'
host_url = 'http://bj.ganji.com'
channel = ''
def get_channel_urls(url, channel):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    links = soup.select('dl.fenlei > dt > a')
    for link in links:
        page_url = host_url + link.get('href')
        channel += (page_url + '\n')
    return channel


channel = get_channel_urls(start_url, channel)