from bs4 import BeautifulSoup
import requests,time,random,pymongo



client = pymongo.MongoClient('localhost',27017)
ganji  = client['ganji']
sheet_table_test = ganji['sheet_table_test']
sheet_table_all_info = ganji['sheet_table_all_info']
sheet_table_fails = ganji['sheet_table_fails']

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Connection':'keep-alive'
}
proxy_list = [
   '124.200.100.50:8080','183.61.236.53:3128','124.202.179.242:8118','124.202.181.186:8118'
]
proxy_ip = random.choice(proxy_list)
proxies ={'http':proxy_ip}



def  get_info(url):#获取详细页基本信息 组成数据库

    time.sleep(10)

    wb_data = requests.get(url,headers=headers)

    if wb_data.status_code == 200:
        # wb_data.encoding('gbk')
        soup = BeautifulSoup(wb_data.text,'lxml')

        titles = soup.title
        times = soup.find_all('i','pr-5')
        types = soup.select('#wrapper > div.content.clearfix > div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(1) > span > a')
        prices = soup.find_all('i','f22')
        ares   = soup.select('#wrapper > div.content.clearfix > div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(3) > a')
        conditions = soup.select('ul.second-det-infor > li ')


        data = {
            'title':titles.text,
            'time' :times[0].text.split() if soup.find_all('i','pr-5') else None,
            'types':types[0].text if soup.select('#wrapper > div.content.clearfix > div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(1) > span > a') else None,
            'price':prices[0].text if soup.find_all('i','f22') else None,
            'ares' :[x.text for x in ares ] if soup.select('#wrapper > div.content.clearfix > div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(3) > a') else None,
            'condition':''.join(conditions[0].text.strip('新旧程度：').split()) if soup.select('ul.second-det-infor > li ') else None,
            'url'  :url,
            'url_id':url.split('/')[-1].split('x.htm')[0]

        }

        # print('标题:{}\n类型:{}   价钱:{}  发布时间:{}\n地点:{}  新旧程度:{}\n网址:{}'.format(data['title'],data['types'],data['price'],
        #                                                             '-'.join(data['time'][0:2]),data['ares'],data['condition'],data['url']))
        print(url)
        sheet_table_all_info.insert(data)

        print('录入OK')

    else:

        print('失效的'  + url)

        data_fails = {
            'url':url
        }
        sheet_table_fails.insert(data_fails)
        print('插入成功')

# get_info(url)

'''
标题
发帖时间
类型
价格
交易地点
'''
