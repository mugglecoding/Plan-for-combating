from bs4 import BeautifulSoup
import requests, time

url = 'http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    'Cookie':'f=n; bangbangid=1080863913546260628; bj58_id58s="ZURHV1Q9anNPMGREMDc2MQ=="; sessionid=dee658e1-65d5-4515-a587-1450a9ecdc4a; id58=c5/njVaN9XY/+ns3BJA/Ag==; als=0; 58home=sz; bdshare_firstime=1452144069496; myfeet_tooltip=end; bangbigtip2=1; city=bj; cookieuid=bf8c14e9-8d9b-4590-8ab2-d2876434d7ff; HISTORY_CATE_IDS=5%2C38484%2C23094%7C%E5%B9%B3%E6%9D%BF%E7%94%B5%E8%84%91%7C2%7C2073; scancat=38484; sale_finalpage_app_open=6; 58app_hide=1; f=n; ipcity=sz%7C%u6DF1%u5733; m58comvp=t08v115.159.229.13; mcity=bj; mcityName=%E5%8C%97%E4%BA%AC; nearCity=%5B%7B%22cityName%22%3A%22%E4%B8%8A%E6%B5%B7%22%2C%22city%22%3A%22sh%22%7D%2C%7B%22cityName%22%3A%22%E5%8C%97%E4%BA%AC%22%2C%22city%22%3A%22bj%22%7D%5D; cookieuid1=c5/ni1aOl1299DjAA9AIAg==; bbsession_uid=1080863913546535503; bbsession_sen=90750292434dc876a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5ea77df14a5a5a5aa8dae2bf319f50a4d6d00d42b5bf24358; bj58_new_session=0; bj58_init_refer=""; bj58_new_uv=8; 58tj_uuid=1b8fc0a1-bba6-4b47-a57f-c6bcaa44bf18; new_session=0; init_refer=; new_uv=8; final_history=24604629984324%2C23940088680633%2C23986528749877%2C24483875226810%2C24063857671738'
}

def get_info(url):
    web = requests.get(url, headers=headers)
    time.sleep(2)
    soup = BeautifulSoup(web.text, 'lxml')
    title = soup.select('div.col_sub.mainTitle > h1')[0].text
    date = soup.select('li.time')[0].text
    price = soup.select('span.price.c_f50')[0].text
    cate = soup.select('span.crb_i > a')[1].text

    areas = soup.select('span.c_25d > a')
    if  areas == []:
        area = '无'
    else:
        list = []
        for a in areas:
            a = a.get_text()
            list.append(a)
        if len(areas) == 1:
            area = list[0]
        else:
            area = list[0] + '-' + list[1]

    types = soup.select('div.wlt_con')
    if types == []:
        type = '个人'
    else:
        type = '商家'

    print('商品标题:%s, 发帖时间:%s, 价格:%s  区域:%s  卖家类型:%s  类目:%s' % (title,date,price,area,type,cate))



list_web = requests.get(url,headers=headers)
soup = BeautifulSoup(list_web.text,'lxml')
list_urls = soup.select('tr > td.img > a')

for list_url in list_urls:
    title_url = list_url.get('href')
    get_info(title_url)