import time
from spider import url_list, item_info

while True:
    links_count = url_list.find().count()
    items_count = item_info.find().count()
    print(links_count,items_count)
    time.sleep(5)