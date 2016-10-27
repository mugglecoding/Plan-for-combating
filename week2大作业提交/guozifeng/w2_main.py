#coding = utf-8
from multiprocessing import Pool
from link_extraction import link_list #导入类目函数
from web_page_parsing import get_links_from,get_item_info,url_list,item_info #导入获取链接和获取页面详情模块和数据库

# db_urls = [item['url'] for item in url_list.find()]
# index_urls = [item['url'] for item in item_info.find()]
# x = set(db_urls)
# y = set(index_urls)
# rest_of_urls = x-y

def get_all_links_from(link):
    for num in range(1,101):
        get_links_from(link,num)


def get_link_from_database(url_list):
    url_infos = []
    for item in url_list.find():
        url_infos.append(item['url'])
    return url_infos


if __name__ == '__main__':
    pool = Pool()
    #获得url
    pool.map(get_all_links_from,link_list.split())
    #获得详情
    pool.map(get_item_info,get_link_from_database(url_list))