import time
from page_parsing import url_list,item_info

while True:
    print(url_list.find().count())
    print(item_info.find().count())
    time.sleep(5)
