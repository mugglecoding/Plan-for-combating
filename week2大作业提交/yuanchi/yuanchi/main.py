from multiprocessing import Pool
from channel_extract import channel_list
from page_parsing import get_links_from


def get_all_links_from(channel):
    for num in range(1,100):#100为上限，如果设置上限过大会导致不断重复刷新
        get_links_from(channel,num)


if __name__ =='__main__':
    pool = Pool()
    pool.map(get_all_links_from,channel_list.split())