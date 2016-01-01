from bs4 import BeautifulSoup
import requests
url='http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'
wb_data=requests.get(url)
soup=BeautifulSoup(wb_data.text,'lxml')
webs=soup.select(' td.img > a')
website_list=([web.get('href') for web in webs])
for website in website_list:
    website_data=requests.get(website)
    soup1=BeautifulSoup(website_data.text,'lxml')
    titles = soup1.select('div.col_sub.mainTitle > h1')[0].text
    counts=soup1.select('ul.mtit_con_left.fl > li.count')[0].text
    dates=soup1.select('ul.mtit_con_left.fl > li.time')[0].text
    prices=soup1.select('span.price.c_f50')[0].text
    seller_types=soup1.select('li > em.medium')
    areas=soup1.select('span.c_25d > a')
    cateloges=soup1.select('span.crb_i > a')[0].text
    print(u'标题：%s,浏览次数：%s,发布日期：%s,价格：%s,区域：%s,卖家类型：%s,类目：%s'%
          (titles,counts,dates,prices,areas,seller_types,cateloges))






