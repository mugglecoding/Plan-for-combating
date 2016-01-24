import time,pymongo
# from phone_number import sheet_info
# from phone_number import sheet_one_url




client = pymongo.MongoClient('localhost',27017)
ganji  = client['ganji']
sheet_table_test = ganji['sheet_table_test']
sheet_table_all_info = ganji['sheet_table_all_info']
sheet_table_fails = ganji['sheet_table_fails']


#-------------------如果中途停止 查询数据库哪些信息还没有爬过--------------------
db_urls = [item['url'] for item in sheet_table_test.find()]
index_urls = [item['url']for item in sheet_table_all_info.find()]
failes_urls = [item['url']for item in sheet_table_fails.find()]

# x = set(db_urls)#所有信息链接集合
# y = set(index_urls)#已经爬取的信息链接集合
# z = set(failes_urls)#已经发现失效的信息链接集合
# rest_of_urls = x - y - z



while True:#循环
    db_urls = [item['url'] for item in sheet_table_test.find()]
    index_urls = [item['url']for item in sheet_table_all_info.find()]
    failes_urls = [item['url']for item in sheet_table_fails.find()]
    x = set(db_urls)#所有信息链接集合
    y = set(index_urls)#已经爬取的信息链接集合
    z = set(failes_urls)#已经发现失效的信息链接集合
    rest_of_urls = x - y - z

    print('详细信息数据库条数:{}************失效信息数据库条数:{}'.format(sheet_table_all_info.find().count(),sheet_table_fails.find().count()))#统计数据库信息数量
    print('剩余:{}'.format(len(rest_of_urls)))
    time.sleep(3)