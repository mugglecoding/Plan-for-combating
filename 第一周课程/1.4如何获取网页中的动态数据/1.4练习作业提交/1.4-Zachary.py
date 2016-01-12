from bs4 import BeautifulSoup
import requests
import json
import time

# ******************** 1.4 练习作业 ********************
# 捉取豆瓣电影的科幻类目的所有信息
# http://movie.douban.com/explore#!type=movie&tag=%E7%A7%91%E5%B9%BB&sort=recommend&page_limit=20&page_start=0
# 包括:
# 1,电影名字 2,海报 3,评分

number = 0
page = 0

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
}


while number == page:
    crawl_url = 'http://movie.douban.com/j/search_subjects?type=movie&tag=%E7%A7%91%E5%B9%BB&sort=recommend&page_limit=20&page_start={}'.format(str(page))
    wb_data = requests.get(crawl_url, headers=headers)
    content = json.loads(wb_data.text).get('subjects')
    for movie in content:
        number += 1
        data = {
            'rate' :movie.get('rate'),
            'title':movie.get('title'),
            'cover':movie.get('cover'),
        }
        print(number, data)
    page += 20
    time.sleep(2)
