from bs4 import BeautifulSoup
import requests
import time
import pymongo


# spider1
# http://bj.ganji.com/jiaju/a2o3/ shan
# http://bj.ganji.com/jiaju/o3/
def get_links_from(channel, pages, who_sells='o'):
    list_view = '{}{}{}/'.format(channel, pages,who_sells)
    wb_data = requests.get(list_view)
    soup = BeautifulSoup(wb_data.text,'lxml')
    for link in soup.select()
