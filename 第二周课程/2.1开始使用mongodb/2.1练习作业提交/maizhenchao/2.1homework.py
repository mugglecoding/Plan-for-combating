from bs4 import BeautifulSoup
import pymongo, requests, time

datas = []
urls = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(i) for i in range(1,4)]
headers = {
    'Cookie':'abtest_ABTest4SearchDate=b; OZ_1U_2282=vid=v687f323752f93.0&ctime=1452520903&ltime=1452520901; OZ_1Y_2282=erefer=-&eurl=http%3A//bj.xiaozhu.com/search-duanzufang-p1-0/&etime=1452520758&ctime=1452520903&ltime=1452520901&compid=2282; __utma=29082403.52157338.1451750181.1451839995.1452520761.5; __utmb=29082403.2.10.1452520761; __utmc=29082403; __utmz=29082403.1451750181.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER'
}
client = pymongo.MongoClient('localhost',27017)
xiaozhu = client['xiaozhu']
house_data = xiaozhu['house_data']

def get_info(url,info=None):
    web = requests.get(url,headers=headers)
    time.sleep(1)
    soup = BeautifulSoup(web.text,'lxml')
    titles = soup.select('.result_title')
    adds = soup.select('em.hiddenTxt')
    imgs = soup.select('.lodgeunitpic')
    rents = soup.select('.result_price > i')
    lorder_imgs = soup.select('.landlordimage')

    if info == None:
        for title, add, img, rent, lorder_img in zip(titles, adds, imgs, rents, lorder_imgs):
            info = {
                'title':title.text,
                'address':add.text.split('\n')[-1].strip(),
                'img':img.get('lazy_src'),
                'rent':int(rent.text),
                'lorder_img':lorder_img.get('lazy_src')
            }
            datas.append(info)
        return datas

for url in urls:
    get_info(url)

for data in datas:
   house_data.insert_one(data)

for item in house_data.find({'rent':{'$gte':500}}):
    print(item)