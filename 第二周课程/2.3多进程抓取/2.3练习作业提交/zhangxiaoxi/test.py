# -*- coding:utf-8 -*-
import pymongo
client =pymongo.MongoClient('localhost',27017)
walden=client['58shoujihao']
url_list=walden['url_list']
content_list=walden['content_list']

for href in content_list.find({}, {'url' : 1}):
    if href in url_list.find({}, {'url' : 1}):
        print 'have'
    else:
        print href

