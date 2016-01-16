from bs4 import BeautifulSoup
import requests
import time

#构建函数,爬去每一个商品详情页面的内容
def web58_prase(url):
    web_data   = requests.get(url,headers=headers)
    soup       = BeautifulSoup(web_data.text,'lxml')
    category = soup.select('#header > div.breadCrumb.f12 > span:nth-of-type(3) > a')[0].text
    title    = soup.select('h1')[0].text
    view      = soup.select('#totalcount')[0].text
    post_time = soup.select('li.time')[0].text
    price     = soup.select('span.price')[0].text
    area      = u'北京' if soup.select('span.c_25d > a:nth-of-type(1)')==[] else soup.select('span.c_25d > a:nth-of-type(1)')[0].text
    type = u'个人' if  soup.select('span.red')[1].text.lstrip()==''  else u'商家'
    print(u'类目:%s, 标题:%s, 发布时间:%s, 浏览量:%s, 价格:%s 卖家类型:%s 地区:%s' % (category, title, post_time,  view, price, type, area))
    time.sleep(1)

#首页信息
start_url     = 'http://bj.58.com/pbdn/?PGTID=0d409654-0000-1f55-c7ec-19d266813a69&ClickID=1'
headers       = {
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
                }
web_data_list = requests.get(start_url,headers=headers)
content       = web_data_list.text
soup          = BeautifulSoup(content,'lxml')
hrefs         = soup.select('td.img > a')
number        = 0

#由首页信息获取的所有商品链接调用函数爬去所有页面的商品信息
for href in hrefs:
    url = href.get('href')
    web58_prase(url)
    number += 1

#打印总数目
print(u'爬取的页面总数为:%s' % number)