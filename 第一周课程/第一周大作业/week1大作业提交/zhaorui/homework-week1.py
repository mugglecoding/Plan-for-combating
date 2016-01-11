from bs4 import BeautifulSoup
import lxml
import requests
import time

url ='http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'

wb_data = requests.get(url)
soup = BeautifulSoup(wb_data.text, 'lxml')

product_urls = soup.select('td.img > a')
urls_list=([product_url.get('href') for product_url in product_urls])

for urls in urls_list:

    def product_info(urls):
        product_data=requests.get(urls)
        soup_p = BeautifulSoup(product_data.text,'lxml')
        product_dates    = soup_p.select('ul.mtit_con_left.fl > li.time')
        product_prices   = soup_p.select('div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li >'
                                        ' div.su_con > span.price.c_f50')
        product_salors   = soup_p.select('div.num_tan_main > div.num_tan_text > p.c_666 > span.red')
        product_areas    = soup_p.select('div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li > '
                                        'div.su_con > span > a')
        product_categories= soup_p.select('div.breadCrumb.f12 > span.crb_i > a')
        product_summary = soup_p.select('div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li > div.su_tit')
        #print(product_summary)

        choice_list=[]
        for choice in product_summary:
            choice = choice.get_text

        if '区域' in choice_list:
            for product_date,product_price, product_salor, product_area, product_category in zip(product_dates, product_prices,
                                                                                                product_salors,product_areas,product_categories):
                product_salor = product_salor.get_text().strip()
                if len(product_salor[0:])==0:
                    infor={
                        'date':product_date.get_text(),
                        'price':product_price.get_text(),
                        'salor': '个人',
                        'area':product_area.get_text(),
                        'category':product_category.get_text()

                    }
                else:
                    infor={
                        'date': product_date.get_text(),
                        'price':product_price.get_text(),
                        'salor':product_salor[0:],
                        'area': product_area.get_text(),
                        'category':product_category.get_text()
                    }
        else:
            for product_date,product_price, product_salor, product_area, product_category in zip(product_dates, product_prices,
                                                                                                product_salors,product_areas,product_categories):
                product_salor = product_salor.get_text().strip()
                if len(product_salor[0:])==0:
                    infor={
                        'date':product_date.get_text(),
                        'price':product_price.get_text(),
                        'salor': '个人',
                        'area':'空白',
                        'category':product_category.get_text()

                    }
                else:
                    infor={
                        'date': product_date.get_text(),
                        'price':product_price.get_text(),
                        'salor':product_salor[0:],
                        'area': '空白',
                        'category':product_category.get_text()
                    }
        print(infor)
        time.sleep(1)
    product_info(urls)







