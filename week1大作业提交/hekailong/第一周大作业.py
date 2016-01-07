from bs4 import BeautifulSoup
import requests
import time
url = 'http://bj.58.com/pbdn/1/?PGTID=0d305a36-0000-1e96-9601-c083f8999a80&ClickID=1'
wb_data = requests.get(url)
soup = BeautifulSoup(wb_data.text,'lxml')


titles = soup.select(' tr > td.t > a.t')
prices = soup.select(' tr > td > b')
addresses = soup.select(' tr > td.t > span.fl > a')
sellerurlfirst = soup.select(' tr > td.t > a.t')


for title,price,address,sellerurl in zip(titles,prices,addresses,sellerurlfirst):
    info = {
        'title':title.get_text(),
        'price':price.get_text()+'元',
        'address':address.get_text(),
        'sellerurl':sellerurl.get('href')


    }


    #获取卖家信息
    seller_url= info['sellerurl']
    seller_data = requests.get(seller_url)
    sellersoup = BeautifulSoup(seller_data.text,'lxml')
    issuedates = sellersoup.select('#index_show > ul.mtit_con_left.fl > li.time')
    pageviews = sellersoup.select('#index_show > ul.mtit_con_left.fl > li.count')
    catagries = sellersoup.select('#header > div.breadCrumb.f12 > span:nth-of-type(3) > a')
    seller_types = u'商家' if sellersoup.select('#divOwner > ul > li > em') else u'个人'
    #print(seller_types)

    for issuedate,pageview,catagry,seller_type in zip(issuedates,pageviews,catagries,seller_types):
        infonext = {
        'issuedate':issuedate.get_text(),
        'pageview':pageview.get_text(),
        'catagry':catagry.get_text(),
        'seller_type':seller_types


        }
    info.update(infonext)
    info.pop('sellerurl')
    print(info)
    time.sleep(2)