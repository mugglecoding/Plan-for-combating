from multiprocessing import Pool
from channel_extact import channel_list
from page_parasing import get_links_from,get_item_info,url_list


def get_all_links_from(channel):
    for i in range(1,200):
        get_links_from(channel,i)

def get_all_item_info():
    for item in url_list.find():
        get_item_info(item['url'])


if __name__ == '__main__':
    pool = Pool()
    pool.map(get_all_links_from,channel_list.split())

get_all_item_info()