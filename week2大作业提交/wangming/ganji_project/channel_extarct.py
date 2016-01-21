# _*_ coding:utf-8 _*_
import io
import sys
from bs4 import BeautifulSoup
import requests
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')     # 改变标准输出的默认编码

start_url = 'http://bj.ganji.com/wu/'
host_url = 'http://bj.ganji.com'

def get_channels_url(start_url):
    web_data = requests.get(start_url)
    web_data.encoding = 'utf-8'        # 以utf-8编码输出网页解码内容
    soup = BeautifulSoup(web_data.text, 'lxml')
    links = soup.select('div.main-pop > dl > dt > a')
    for link in links:
        channel_url = host_url + link.get('href')
        print(channel_url)

get_channels_url(start_url)

channel_list = '''
    http://bj.ganji.com/shouji/
    http://bj.ganji.com/shoujihaoma/
    http://bj.ganji.com/shoujipeijian/
    http://bj.ganji.com/bijibendiannao/
    http://bj.ganji.com/taishidiannaozhengji/
    http://bj.ganji.com/diannaoyingjian/
    http://bj.ganji.com/wangluoshebei/
    http://bj.ganji.com/shumaxiangji/
    http://bj.ganji.com/youxiji/
    http://bj.ganji.com/xuniwupin/
    http://bj.ganji.com/jiaju/
    http://bj.ganji.com/jiadian/
    http://bj.ganji.com/zixingchemaimai/
    http://bj.ganji.com/rirongbaihuo/
    http://bj.ganji.com/yingyouyunfu/
    http://bj.ganji.com/fushixiaobaxuemao/
    http://bj.ganji.com/meironghuazhuang/
    http://bj.ganji.com/yundongqicai/
    http://bj.ganji.com/yueqi/
    http://bj.ganji.com/tushu/
    http://bj.ganji.com/bangongjiaju/
    http://bj.ganji.com/wujingongju/
    http://bj.ganji.com/nongyongpin/
    http://bj.ganji.com/xianzhilipin/
    http://bj.ganji.com/shoucangpin/
    http://bj.ganji.com/baojianpin/
    http://bj.ganji.com/laonianyongpin/
    http://bj.ganji.com/gou/
    http://bj.ganji.com/qitaxiaochong/
    http://bj.ganji.com/xiaofeika/
    http://bj.ganji.com/menpiao/
'''