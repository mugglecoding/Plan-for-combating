#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'stone'

import time
from pages import item_info
from pages import url_list
while True:
    print 'item_info:',item_info.find().count()
    print 'url_list:',url_list.find().count()
    time.sleep(5)
