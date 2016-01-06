# -*- coding: utf-8 -*-

import json
import random
import requests
import time

page_start = 0
headers = {
    'Host': 'movie.douban.com',
    'Refer': 'http://movie.douban.com/explore',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
}
# 从http://cn-proxy.com/上获取的代理ip，速度慢时需要重新去网站获取更新
proxy_list = [
    'http://120.24.221.241:8888',
    'http://121.69.36.122:8118',
    'http://124.200.33.146:8118',
]
try:
    while True:
        crawl_url = u'http://movie.douban.com/explore#!type=movie&tag=科幻&sort=recommend&page_limit=20&page_start=%s' % page_start
        proxy_ip = random.choice(proxy_list) # 随机获取代理ip
        proxies = {
            'http': proxy_ip,
        }
        content = requests.get(crawl_url, headers=headers, proxies=proxies).text
        rst = json.loads(content)
        subjects = rst.get('subjects')
        if subjects:
            page_start += 20
            for subject in subjects:
                title = subject.get('title')
                cover = subject.get('cover')
                rate = subject.get('rate')
                print(u'电影名称: %s, 封面: %s, 评分:%s' % (title, cover, rate))
            time.sleep(2)
        else:
            # 若取不到最新的数据则退出循环
            break
except KeyboardInterrupt: # ctrl+c 退出
    print(u'手动结束!')
finally:
    print(u'数据获取结束!共获取%s条数据' % page_start)