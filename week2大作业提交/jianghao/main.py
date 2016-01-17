from multiprocessing import Pool
from channel_extract import channel_list
from page_parsing import get_links_from,get_item_info
from page_parsing import url_list

def get_all_links_from(channel):
    for num in range(1,101):
        get_links_from(channel,num)



if __name__ == '__main__':
    pool = Pool()
    #pool.map(get_all_links_from,channel_list.split())
    #pool.map(get_item_info,a)
    pool.map(get_item_info,[item['url'] for item in url_list.find()])