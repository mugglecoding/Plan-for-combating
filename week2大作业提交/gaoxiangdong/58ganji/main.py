from multiprocessing import Pool
from channel_extact import channel_list
import pages_parsing


def get_all_links_from (channel):
    for i in range(1,100):
        pages_parsing.get_links_from(channel,i)


# 查询url_list表，从表中获得所有的url
def find_url_list(url_list):
    url_infos = []
    for item in url_list.find():
        url_infos.append(item)
    return url_infos


if __name__ == '__main__':
    pool = Pool()
    #获得url
    pool.map(get_all_links_from, channel_list.split())
    # 获得商品详情
    pool.map(pages_parsing.get_item_info, find_url_list(pages_parsing.url_list))

