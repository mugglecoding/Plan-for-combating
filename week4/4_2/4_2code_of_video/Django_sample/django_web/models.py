from django.db import models
from mongoengine import *
from mongoengine import connect
connect('wbsite', host='127.0.0.1', port=27017)

# ORM

class ArtiInfo(Document):
    des = StringField()
    title = StringField()
    scores = StringField()
    tags = ListField(StringField())

    meta = {'collection':'arti_info3'}


for i in ArtiInfo.objects[:1]:
    print(i.title,i.des,i.scores,i.tags)




