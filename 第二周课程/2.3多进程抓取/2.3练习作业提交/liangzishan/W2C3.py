# ******************** 2.3 练习作业 ********************
# 假设在抓取过程中会遇到网络问题而导致程序停止,
# 在程序中设计一个功能保证数据库中开始抓取的数据不会重复.

# status : 1:已抓取网页数据; 0:未抓取该页面数据;
'''
import pymongo

client = pymongo.MongoClient('localhost', 27017)
local_db = client['local_db']
phone_num_58_col = local_db['phone_num_58_col']
test_col = local_db['test_col']

for doc in local_db.phone_num_58_col.find():
    doc.update({'status':0})
    test_col.update({'status':0}, data)

for doc in test_col.find({'status':0}):
    print('deal with somethins and change the status.')
    test_col.update({'status':0}, {'status':1})
'''