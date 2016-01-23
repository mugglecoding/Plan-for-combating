#Author_yaobozhang
from multiprocessing import Pool
from get_item_urls import *
from normal_item_parsing import *

def get_all_items_from(channel):
    for num in range(1,100):
        get_links_from(channel,num,'')
        get_links_from(channel,num,'a2')



if __name__=='__main__':
    pool = Pool()
    pool.map(get_all_items_from,item_url_lists)