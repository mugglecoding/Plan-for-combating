from bs4 import BeautifulSoup
import requests
url = 'http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'
wb_data =  requests.get(url)
soup = BeautifulSoup(wb_data.text,'lxml')
dizhi1 = soup.select('tbod > tr >td.t > a.t')
dizhi3 = [dizhi2.get('href') for dizhi2 in dizhi1]
for dizhi in dizhi3:
    wb_data = requests.get(dizhi)
    xiangqing = BeautifulSoup(wb_data.text,'lxml')
    titles = xiangqing.select('div.person_add_top no_ident_top > div.per_ad_left > div.col_sub mainTitle > h1')
    prices = xiangqing.select('div.person_add_top no_ident_top > div.per_ad_left > div.col_sub sumary > ul > li > div.su_con > span')
    shijian = xiangqing.select('div.person_add_top no_ident_top > div.per_ad_left > div.col_sub mainTitle > div.mtit_con c_999 f12 clearfix > ul.mtit_con_left fl > li')
    quyus = xiangqing.select('div.col_sub sumary > ul.suUl > li.su_tit')
    types = xiangqing.select('div.f1 > ul.userinfo > ul.vcard > li')
    for title,price,Time,quyu,type in zip(titles,prices,shijian,quyu,types):
        data = {
            'title':title.get_text(),
            'price':price.get_text(),
            'Time':Time.get_text(),
            'quyu':quyu.get_text(),
            'type':type.get_text(),
        }
    print(data)
