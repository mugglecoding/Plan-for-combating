from multiprocessing import Pool
from channel_extarct import channel_list
from page_parsing import url_list
from page_parsing import get_url_link
from page_parsing import get_item_info
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')     # 改变标准输出的默认编码

def get_all_links(channel):
    for num in range(1, 10):
        try:
            get_url_link(channel, num, who_sells=0)
            get_url_link(channel, num, who_sells=1)
        except:
            pass



if __name__ == '__main__':
    pool = Pool()
    # pool.map(get_all_links, channel_list.split())
    try:
        for item_url in url_list.find():
            print(item_url['url'])
            get_item_info(item_url['url'])
    except:
        pass

