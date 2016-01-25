from multiprocessing import Pool


import time,pymongo
from page_info import get_info

#####################################################
client = pymongo.MongoClient('localhost',27017)
ganji  = client['ganji']
sheet_table_test = ganji['sheet_table_test']#所有详细链接的数据库
sheet_table_all_info = ganji['sheet_table_all_info']#所有详细信息的数据库
sheet_table_fails = ganji['sheet_table_fails'] #失效链接的数据库


#-------------------如果中途停止 查询数据库哪些信息还没有爬过--------------------
db_urls = [item['url'] for item in sheet_table_test.find()]
index_urls = [item['url']for item in sheet_table_all_info.find()]
failes_urls = [item['url']for item in sheet_table_fails.find()]

x = set(db_urls)#所有信息链接集合
y = set(index_urls)#已经爬取的信息链接集合
z = set(failes_urls)#已经发现失效的信息链接集合
rest_of_urls = x - y - z


# # def get_all_links_from(channel):#获取所有分类信息的详细页链接
#
#     for i in range(1,151):
#         time.sleep(1)
#         get_info_link_from(channel,i)#从分类网页列表中获取详情页链接





if __name__ == '__main__':
     pool = Pool()

     pool.map(get_info,[x for x in list(rest_of_urls)])






