from multiprocessing import Pool
from get_index import channel_list
import spider

def get_all_links(channel):
    for seller_num in range(1, 3):
        for page in range(1, 100):
            spider.get_link(channel, page, seller_num)

def get_all_item(url_data):
    url = url_data['url']
    spider.get_info(url, url_data['seller_type'])

if __name__ == '__main__':
    pool = Pool()
    pool.map(get_all_links, channel_list)
    pool.map(get_all_item, spider.url_list.find())