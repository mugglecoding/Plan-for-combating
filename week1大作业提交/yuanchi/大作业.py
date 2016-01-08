from bs4 import BeautifulSoup
import requests
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',
}

def detail_info(detail_url):
    detail_db = requests.get(detail_url,headers=headers)
    detail_soup = BeautifulSoup(detail_db.text,'lxml')
    title= detail_soup.select('div.col_sub.mainTitle > h1')[0].get_text()
    release_time = detail_soup.select('li.time')[0].get_text()
    price = detail_soup.select('span.price.c_f50')[0].get_text()
    cate = detail_soup.select('span.crb_i')[0].get_text()

    #经观察区域信息有3种情况，1:无区域信息，2:只有大区域，3:大区域和小区域
    areas = detail_soup.select('span.c_25d > a')
    if  areas == []:
        area = '无'
    else:
        list = []
        for i in areas:
            i = i.get_text()
            list.append(i)
        if len(areas) <= 1:
            area = list[0]
        else:
            area = list[0] + '-' + list[1]

    #获取浏览量，经老师提示，浏览量在js里动态生成，通过获取特定id获取js网址从而解析浏览量。
    id = detail_url.split('x.')[0].split('/')[-1]#字符串分割使用split方法分割出所需id。
    view_url = 'http://jst1.58.com/counter?infoid={}'.format(str(id))
    view_db = requests.get(view_url)
    view_text = view_db.text
    view = view_text.split('=')[2]

    #获取卖家类型,如果是商家的话会有商家介绍这个div，否则就是个人
    types = detail_soup.select('div.wlt_con')
    if types == []:
        type = '个人'
    else:
        type = '商家'
    print('商品标题:'+title+'|','浏览量:'+view+'|','发帖时间:'+release_time+'|','价格:'+price+'元|','卖家类型:'+type+'|','区域:'+area+'|','类目:'+cate)
    print('-------------------------------------------------------------------------------------------------------------------------------------------------------')
'''
#获取题目要求第6页中的信息
page = 6
main_url = 'http://bj.58.com/pbdn/pn%s/' % page
main_db = requests.get(main_url)
soup = BeautifulSoup(main_db.text, 'lxml')
details = soup.select('td.t > a.t')
for detail in details:
    detail_url = detail.get('href')#获取detail_url
    detail_info(detail_url)
'''
for page in range(1,100):
    main_url = 'http://bj.58.com/pbdn/pn%s/' %page
    main_db = requests.get(main_url)
    soup = BeautifulSoup(main_db.text, 'lxml')
    details = soup.select('td.t > a.t')
    for detail in details:
        detail_url = detail.get('href')#获取detail_url
        detail_info(detail_url)
        #time.sleep(2)
