from bs4 import BeautifulSoup
import requests,time,random,pymongo

client = pymongo.MongoClient('localhost',27017)
ganji  = client['ganji']
sheet_table_test = ganji['sheet_table_test']


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Connection':'keep-alive'
}
proxy_list = [
'121.69.24.22:8118','121.69.25.2:8118','121.69.23.134:8118'
]
proxy_ip = random.choice(proxy_list)
proxies ={'http':proxy_ip}


def get_info_link_from(channel,page,whosells='o'):#获取详细页的链接
    time.sleep(1)
    url = '{}{}{}'.format(channel,whosells,page)
    print('*******************'+ url +'******************')#显示第几页

    wb_data = requests.get(url,headers = headers,proxies=proxies)
    soup = BeautifulSoup(wb_data.text,'lxml')


    if soup.find('ul','pageLink'):#判断是否是最后一页

        info_links =soup.select('.list-bigpic dt a')

        for info_link in info_links:

            if len(info_link.get('href')) < 60:#符合条件的链接
                data = {
                    'url':info_link.get('href')
                }
                sheet_table_test.insert_one(data)
                #print(data)

    else:
        pass



# print(len([x for x in sheet_table_test.find()]))
# get_info_link_from('http://bj.ganji.com/nokia/',1)





