#!/usr/bin/env python
#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import time

def get_links_from(who_sells):
    urls = []
    url = 'http://bj.58.com/pbdn/{}/pn2/'.format(who_sells)
    wb_data = requests.get(url)
    if wb_data.status_code == 200:
        soup = BeautifulSoup(wb_data.text, 'lxml')
        for link in soup.select('td.t a.t'):
            urls.append(link.get('href'))
    return urls


def get_views_from(url):
    # url后面带有问号和参数，取问号前的url
    url_path = url.split("?")[0]
    # 取最后一节url信息，其带有id信息
    url_last_part = url_path.split('/')[-1]
    # 去掉后面的x.shtml,得到id
    info_id = url_last_part.strip('x.shtml')
    api = 'http://jst1.58.com/counter?infoid={}'.format(info_id)
    # 这个是找到了58的查询接口，不了解接口可以参照一下新浪微博接口的介绍
    # 浏览量的抓取做了反爬虫，因此加上header信息，不然返回为空
    headers = {
        'User-Agent':r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
        'Cookie':r'id58=c5/ns1ct99sKkWWeFSQCAg==; city=bj; 58home=bj; ipcity=yiwu%7C%u4E49%u4E4C%7C0; als=0; myfeet_tooltip=end; bj58_id58s="NTZBZ1Mrd3JmSDdENzQ4NA=="; sessionid=021b1d13-b32e-407d-a76f-924ec040579e; bangbigtip2=1; 58tj_uuid=0ed4f4ba-f709-4c42-8972-77708fcfc553; new_session=0; new_uv=1; utm_source=; spm=; init_refer=; final_history={}; bj58_new_session=0; bj58_init_refer=""; bj58_new_uv=1'.format(str(infoid)),
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host':'jst1.58.com',
        'Referer':r'http://bj.58.com/pingbandiannao/{}x.shtml'.format(info_id)
    }
    r = requests.get(api, headers=headers)
    # 判断状态码，检查是否被网站封ip
    if r.status_code == 200:
        return js.text.split('=')[-1]
    return 0


def get_item_info(who_sells=0):
    urls = get_links_from(who_sells)
    for url in urls:
        wb_data = requests.get(url)
        # 判断状态码，检查是否被网站封ip
        if wb_data.status_code != 200:
            continue
        
        soup = BeautifulSoup(wb_data.text, 'lxml')
        
        prices = soup.select('.price')
        areas = soup.select('.c_25d')
        dates = soup.select('.time')
        
        data = {
            'title': soup.title.text,
            # 检查价格标签是否存在，存在则取，不存在设置默认值
            'price': prices[0].text if len(prices) > 0 else 0,
            # 检查区域标签是否存在，存在则取，不存在设置默认值
            'area' : list(areas[0].stripped_strings) if len(areas) > 0 else [],
            # 检查时间标签是否存在，存在则取，不存在设置默认值
            'date' : dates[0].text if len(dates) > 0 else "",
            'cate' : '个人' if who_sells == 0 else '商家',
            # 浏览量是通过脚本生成的，不能从源代码直接取到，需要从network找到请求信息，模拟请求获取
            'views': get_views_from(url)
        }
        print(data)

# 只有直接执行脚本才会运行下面的函数，如果其他文件引用这个文件，下面的函数不会执行
if __name__ == '__main__':
    get_item_info()
