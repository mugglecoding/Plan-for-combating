from django.db import models

from mongoengine import *
# Create your models here.
class ItemInfo(Document):
    title = StringField()
    url = StringField()
    pub_date = StringField()
    area = ListField(StringField())
    cates = ListField(StringField())
    look = StringField()
    time = StringField()
    price = IntField()
    meta = {'collection':'item_infoS'}
