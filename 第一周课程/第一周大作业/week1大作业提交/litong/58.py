from bs4 import BeautifulSoup
import requests
import time


url = 'http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'

url1 = 'http://jst1.58.com/counter?infoid='


#u1 = 'http://bj.58.com/pingbandiannao/24063001373753x.shtml?adtype=1&PGTID=0d305a36-0000-15fc-9fd4-6d9b525b011f&entinfo=24063001373753_0&psid=115136530190322804712479354&iuType=q_2&ClickID=13'





def get_JS_link(content1,content2):

    startIndex = content1.index('entinfo') + 8
    endIndex = startIndex + 14
    JS_link = content2 + content1[startIndex:endIndex]
    return (JS_link)



def get_viewCount(url):
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text, 'lxml')
    views = soup.select('body')
    count = str(views[0])
    start = count.index('total') + 6
    end = count.index('</p>')
    viewCount = count[start: end]
    return viewCount



def get_detailedInfo(url, detailedData=None):

    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text, 'lxml')

    dates = soup.select('ul.mtit_con_left.fl > li.time')
    prices = soup.select('div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li > div.su_con > span.price.c_f50')
    types = soup.select('div.num_tan > div.num_tan_in > div.num_tan_main > div.num_tan_text > p.c_666 > span.red')
    areas = soup.select('div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li > div.su_con > span > a:nth-of-type(1)')

    decide = soup.select('div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li > div.su_tit')

    list=[]
    for dec in decide:
        dec = dec.get_text()
        list.append(str(dec[0:2]))

    if detailedData==None:

        if '区域' in list:

            for date, price, type, area in zip(dates, prices, types,areas):

                view_url = get_JS_link(url,url1)
                viewCount = get_viewCount(view_url)

                type = type.get_text().strip()

                if len(type[1:-1]) == 0:
                    detailedData = {
                        'viewCount': viewCount,
                        'date': date.get_text(),
                        'price': price.get_text(),
                        'type': '个人',
                        'area': area.get_text()
                }
                else:
                    detailedData = {
                        'viewCount': viewCount,
                        'date': date.get_text(),
                        'price': price.get_text(),
                        'type': type[1: -1],
                        'area': area.get_text()
                    }

            return detailedData

        else:

            for date, price, type in zip(dates, prices, types):

                view_url = get_JS_link(url,url1)
                viewCount = get_viewCount(view_url)

                type = type.get_text().strip()

                if len(type[1:-1]) == 0:
                    detailedData = {
                        'viewCount': viewCount,
                        'date': date.get_text(),
                        'price': price.get_text(),
                        'type': '个人',
                        'area': 'not mentioned'
                    }
                else:
                    detailedData = {
                        'viewCount': viewCount,
                        'date': date.get_text(),
                        'price': price.get_text(),
                        'type': type[1:-1],
                        'area': 'not mentioned'
                    }

            return detailedData



def get_info(url, data=None):

    time.sleep(2)
    n = 0

    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text, 'lxml')
    titles = soup.select('td.t > a.t')

    if data==None:
        for title in titles:

            data = {
                'title': title.get_text().strip()
            }

            homepage = title.get('href')
            detailedData = get_detailedInfo(homepage)

            print(data)
            print(detailedData)
            n += 1
            print (n, '--------------------------------------------- \n')


get_info(url)

