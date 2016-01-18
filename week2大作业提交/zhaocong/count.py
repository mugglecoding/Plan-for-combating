# -*- coding: utf-8 -*-
import time
from page_parsing import ganji_links
from page_parsing import  ganji_item

while True:
    print(ganji_item.find().count())
    print(ganji_links.find().count())
    time.sleep(5)