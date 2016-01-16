#encoding:utf-8
import time
from page_parsing import *

while True:
    print('个人发布信息数量：',url_list.find().count())
    print('商家发布信息数量：',url_list_vip.find().count())
    time.sleep(5)