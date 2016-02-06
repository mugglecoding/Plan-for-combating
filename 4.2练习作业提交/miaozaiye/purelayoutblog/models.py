from django.db import models
from mongoengine import *
from mongoengine import connect
import pymongo
# client = pymongo.MongoClient('localhost',27017)
#
# ganji = client['ganji']
# item_info1 = ganji['item_info1']

connect('ganji',host='127.0.0.1',port=27017)

class ItemInfo(Document):
    title = StringField()
    area = StringField()
    url = StringField()
    look = StringField()
    price = StringField()
    cates = StringField()
    pub_date = StringField()

    meta={'collection':'item_info1'}

# for i in ItemInfo.objects:
#     print(i.title,i.area,i.url,i.look)

# Create your models here.

