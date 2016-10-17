#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

# 采用代理，否则打开不了网页
proxies = {"http": "207.62.234.53:8118"}

# 加上请求头，模拟浏览器访问，防止被发现是爬虫
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
}


def download(url):
    r = requests.get(url, proxies=proxies, headers=headers)
    if r.status_code != 200:
        return

    # http://www.example.com/test.png?a=1
    # 第一个split，获取问号前面的字符
    # 第二个split，获取倒数第二个一个斜杠的后面的内容，因为最后一个斜杠后面的字符串都一样，不能用
    filename = url.split("?")[0].split("/")[-2]

    target = "./{}.jpg".format(filename)

    with open(target, "wb") as fs:
        fs.write(r.content)

    print("%s => %s" % (url, target))


def main():
    # 获取1 ~ 10页的图片
    for page in range(1, 10):
        # 找规律，发现只有替换请求链接的page参数即可进入相应页面
        url = "http://weheartit.com/inspirations/beach?page={}".format(page)

        r = requests.get(url, proxies=proxies, headers=headers)

        # 检查是否正常访问，异常访问返回的状态码不是200，异常就跳过
        if r.status_code != 200:
            continue

        # 提取页面的图片，得到地址，然后下载
        soup = BeautifulSoup(r.text, "html.parser")
        imgs = soup.select('img.entry_thumbnail')
        for img in imgs:
            src = img.get("src")
            download(src)

if __name__ == '__main__':
    main()
