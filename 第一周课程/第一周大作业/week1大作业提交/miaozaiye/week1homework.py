from bs4 import BeautifulSoup
import requests
import time


wb_data = requests.get('http://bj.58.com/pbdn/?PGTID=0d305a36-0000-1c42-b93a-b4f3aa748890&ClickID=1')
soup = BeautifulSoup(wb_data.text,'lxml')
urls = soup.select('a.t')
urls1 = []
i = 0

for url in urls:
    url1 = url.get('href')
    urls1.append(url1)


def yon(kwd):             #将soup.select对象处理为字符串
    for k in kwd:
        return k.get_text()

def yoa(kwd):             #将 area 转化为 区域-具体地址 的字符串
    for k in kwd:
        k0 = ''
        for k1 in k.get_text().split('\n'):
            for k11 in k1.strip().split('\t'):
                k0=k0+k11
        return k0

def stype(kwd):           #判断卖家是商家还是个人
    for s in kwd:
        if '店' in s.get_text():
            return 'business'
        elif '公司' in s.get_text():
            return 'business'
        else:
            return 'person'



def get_pageinfo(url):   #主程序
    header = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
    }
    page_data = requests.get(url,headers = header)
    soup = BeautifulSoup(page_data.text,'lxml')

    titles = soup.select('#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.mainTitle > h1')
    views = soup.select('#totalcount')
    times = soup.select('li.time')
    prices = soup.select('span.price.c_f50')
    sellernames = soup.select('#personInfo > div > h3')
    sellertypes = soup.select('#sub_1 > div.descriptionBox > article > p > span')
    areas = soup.select('span.c_25d')
    print ('title = ',yon(titles),'\n','view = ',yon(views),'\n','time = ',yon(times),'\n','price = ',yon(prices),'\n','name = ',yon(sellernames),'\n','sellertype = ',stype(sellertypes),'\n','area = ',yoa(areas))
    info = {
            'title':yon(titles),
            'time' :yon(times),
            'view' :yon(views),
            'price':yon(prices),
            'sellertype':stype(sellertypes),
            'area':yoa(areas),
        }
    return (info)


i = 0
info1 = []
for url in urls1:
    time.sleep(1)
    print (i)
    info1.append(get_pageinfo(url))
    i = i+1

print (info1)

