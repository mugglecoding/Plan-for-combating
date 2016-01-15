import page_parsing
from multiprocessing import Pool
from channel_extract import channel
import pymongo
from page_parsing import ganji_links

client = pymongo.MongoClient('localhost',27017)#建立与mongoDB联系
ganji = client['ganji']
ganji_links = ganji['ganji_links']#建立数据表,存储商品链接
ganji_item = ganji['ganji_itme']#建立数据表,存储商品信息

def get_all_links_from(channel):
    for num in range(1,3):
        if channel.split('/')[-2] == 'shoujihaoma':#不爬取手机号码商品信息
            pass
        else:
            page_parsing.get_links_from(channel,num,'a1')#爬取个人卖家
            page_parsing.get_links_from(channel,num,'a2')#爬取商城卖家
def get_all_item_info(url):
    page_parsing.get_item_info(url)


if __name__ == '__main__':
    pool = Pool()
    urls = []
    pool.map(get_all_links_from,channel.split())
    for url in ganji['ganji_links'].find():#依次读取链接数据库中链接，供map函数使用
        page = url['url'].split()
        pool.map(get_all_item_info,page)





