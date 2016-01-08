from bs4 import BeautifulSoup
import requests

url = 'http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'

headers={
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4',
    'Cookie':'f=n; id58=05dzXVXq2yCWNjzvG22GAg==; __utma=253535702.3048891.1441454876.1441454876.1446559050.2; __utmz=253535702.1446559050.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; undefined=c4791ea6-d854-4c77-a9c6-793f509f0a48; als=0; bj58_id58s="dnQ5M09Jd24wczZINDA3NQ=="; sessionid=e37157b3-0079-4176-8400-bd7d57514e66; city=bj; Hm_lvt_3bb04d7a4ca3846dcc66a99c3e861511=1452174657; Hm_lpvt_3bb04d7a4ca3846dcc66a99c3e861511=1452174657; 58home=zhuzhou; myfeet_tooltip=end; bangbigtip2=1; ipcity=zhuzhou%7C%u682A%u6D32; final_history=24530729180213%2C24483875226810%2C24532365646523%2C23986528749877%2C24548770853438; bj58_new_session=0; bj58_init_refer="http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6"; bj58_new_uv=3; cookieuid=125731de-5eab-4e89-ac9b-8330b94e0e8f; HISTORY_CATE_IDS=5%2C38484%2C23094%7C%E5%B9%B3%E6%9D%BF%E7%94%B5%E8%84%91%7C2%7C2073; 58tj_uuid=ef1b78f4-f328-4294-9545-9257ae814cd0; new_session=0; init_refer=; new_uv=5; sale_list_app_open=2; scancat=38484; device=m; m58comvp=t08v115.159.229.13; bbsession_uid=1080863913548716915; bbsession_sen=8471a9693614e98ea5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5d6be3914a5a5a5aabc032bf3ddd20a4d62428e32a4aec768'
}

def get_attractions(url,headers):
    wb_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(wb_data.text,'lxml')
    viewcount = soup.select('ul.mtit_con_left.fl > li[title="浏览次数"]')
    item = soup.select('div.breadCrumb.f12')
    selfid = soup.select('ul.userinfo')
    return viewcount,item,selfid


yao_data=requests.get(url,headers=headers)
Soup=BeautifulSoup(yao_data.text,"lxml")
#titles = Soup.select('td.t > a[rel="nofollow"]')
titles = Soup.select('li > a > dt.tit > strong')
times = Soup.select('dd.attr > span.img_num')
prices = Soup.select('td.tc > b.pri')
print(titles,times)


#i=0
'''for title,time,price in zip(titles,times,prices):
    if len(title.get_text())>1:
        url1 = title.get('href')
        viewcount,item,selfid = get_attractions(url1,headers)
        data = {
            'title':title.get_text(),
            'time and area':time.get_text(),
            'price':price.get_text(),
            'viewcount':[i.get_text() for i in viewcount],
            'item':[i.get_text() for i in item],
            'selfid':[i.get_text() for i in selfid]
         }
        i+=1
        #print(data)

#print(i)'''

