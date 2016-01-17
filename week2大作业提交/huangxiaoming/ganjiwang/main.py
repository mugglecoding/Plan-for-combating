from multiprocessing import Pool
from channel_extract import channel_list
import page_parsing

def get_all_links_from(channel):
    for who_sell in range(1, 3):
        for page in range(1, 201):
            page_parsing.get_links_from(channel, page, who_sell)

def get_all_item_info(url):
    get_item_info(url)

if __name__=="__main__":
    pool = Pool()
    pool.map(get_all_links_from,channel_list.split())
    for url in url_list.find():
        page = url['url']
        pool.map(get_all_item_info,page)
