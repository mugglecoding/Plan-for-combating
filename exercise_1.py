from bs4 import BeautifulSoup
import requests



def get_detail(url):
    path = requests.get(url)
    soup = BeautifulSoup(path.text, 'lxml')

    title = soup.select('div.col_sub mainTitle > h1')
    count = soup.select('em#totalcount')
    time = soup.select('li.time')[0].get_text()
    price = soup.select('span.price c_f50')
    seller = soup.select('div.wlt_con')
    area = soup.select('span."c_25d"')
    cate = soup.select('spn.crb_i')

    print('商品标题:'+str(title))
    print('浏览量:'+str(count))
    print('发帖时间:'+str(time))
    print('价格:'+str(price))
    print('卖家类型:'+str(seller))
    print('区域:'+str(area))
    print('类目:'+str(cate))

    #print(title,count,time,price,seller,area,cate)

url = 'http://bj.58.com/pingbandiannao/24405193223994x.shtml?psid=115102221190305411008274206&entinfo=24405193223994_0&iuType=z_2&PGTID=0d305a36-0000-10ee-8096-89fd9f25a35e&ClickID=6&adtype=3'
get_detail(url)
print("\n----------\n")
url = 'http://bj.58.com/pingbandiannao/24537316835392x.shtml?psid=115102221190305411008274206&entinfo=24537316835392_0&iuType=p_0&PGTID=0d305a36-0000-10ee-8096-89fd9f25a35e&ClickID=7'
get_detail(url)

# url = 'http://bj.58.com/pbdn/?PGTID=0d305a36-0000-1408-a3f8-64bb8c054c8c&ClickID=1'
# path = requests.get(url)
# soup = BeautifulSoup(path.text, 'lxml')
#
# details = soup.select('td.t > a.t')
# count = 0
# for detail in details:
#     detail = detail.get('href')
#     count += 1
#     print(detail,count)
#     get_detail(detail)

'''
商品标题
浏览量
发帖时间
价格
卖家类型(个人还是商家)
区域
类目
'''