from bs4 import BeautifulSoup
import requests
import pymongo

client = pymongo.MongoClient('localhost',27017)
ganji = client['ganji']
tab_channel_list = ganji['channel_list']
start_url = 'http://bj.ganji.com/wu/'



def get_index_url(url):
    url_host = 'http://bj.ganji.com'
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    channels = soup.select('dl.fenlei > dt > a')
    for channel in channels:
        page_url = url_host + channel.get('href')

        channel_data = {
            'channel_url':page_url,
        }
        tab_channel_list.update(channel_data,{'$set':channel_data},upsert=True)
        #第三个upsert参赛,默认false,表示insert if not exist

if __name__ == '__main__':
    get_index_url(start_url)

channel_list=''
for i in tab_channel_list.find() :
    channel_list = i['channel_url']+'\n'+channel_list
print(channel_list)
#wrapper > div.content > div:nth-child(2) > div.sider.width5 > dl > dt > a
#wrapper > div.content > div:nth-child(2) > div.sider.width5 > dl > dd > a:nth-child(1)