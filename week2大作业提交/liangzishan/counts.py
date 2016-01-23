import pymongo
import time

client   = pymongo.MongoClient('localhost', 27017)
local_db = client['local_db']
w2_chnlUrl_col  = local_db['w2_chnlUrl_col']
w2_itmUrl_col   = local_db['w2_itmUrl_col']
w2_itmInfo_col  = local_db['w2_itmInfo_col']

while True:
    print('Done urls from Chnl: ' % + w2_chnlUrl_col.find({'url_st': True}).count())
    print('Done itm urls: ' + w2_itmUrl_col.find().count())
    print('Done itm infos: ' + w2_itmUrl_col.find({'itm_st': True}).count())
    print('Check itm infos' + w2_itmInfo_col.find().count())
    time.sleep(60)