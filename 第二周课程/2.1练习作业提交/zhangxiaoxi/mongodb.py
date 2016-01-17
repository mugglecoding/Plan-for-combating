import pymongo
client =pymongo.MongoClient('localhost',27017)
walden=client['58shoujihao']
sheet_tab=walden['url_list']
for item in sheet_tab.find():

    print (item.get('url'))
'''
{'price':{'$lt':500}}
'''