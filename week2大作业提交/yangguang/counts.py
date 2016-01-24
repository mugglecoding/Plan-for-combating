import time
from pages_parsing import tab_url_list

while True:
    print(tab_url_list.find().count())
    time.sleep(3)