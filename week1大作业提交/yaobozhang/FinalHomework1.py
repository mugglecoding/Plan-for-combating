from bs4 import BeautifulSoup
import requests

url = 'http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36',
    'Cookie':'userid360_xml=FF702FDE6C0922198B873150C23BE3AD; time_create=1454766912281; myfeet_tooltip=end; f=n; id58=05dzXVXq2yCWNjzvG22GAg==; __utma=253535702.3048891.1441454876.1441454876.1446559050.2; __utmz=253535702.1446559050.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; undefined=c4791ea6-d854-4c77-a9c6-793f509f0a48; als=0; bj58_id58s="dnQ5M09Jd24wczZINDA3NQ=="; sessionid=e37157b3-0079-4176-8400-bd7d57514e66; city=bj; Hm_lvt_3bb04d7a4ca3846dcc66a99c3e861511=1452174657; Hm_lpvt_3bb04d7a4ca3846dcc66a99c3e861511=1452174657; ipcity=zhuzhou%7C%u682A%u6D32; bj58_new_session=0; bj58_init_refer=""; bj58_new_uv=1; 58tj_uuid=ef1b78f4-f328-4294-9545-9257ae814cd0; new_session=0; init_refer=http%253A%252F%252Fbj.58.com%252Fpbdn%252F%253FPGTID%253D0d100000-0000-1121-f41b-137aeef068b7%2526ClickID%253D6; new_uv=3; f=n'
}

def get_attractions(url,headers):
    wb_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(wb_data.text,'lxml')
    viewcount = soup.select('ul.mtit_con_left.fl > li[title="浏览次数"]')
    item = soup.select('div.breadCrumb.f12')
    selfid = soup.select('div.fl > ul.userinfo > li > a.tx')
    return viewcount,item,selfid


yao_data=requests.get(url,headers=headers)
Soup=BeautifulSoup(yao_data.text,"lxml")
titles = Soup.select('table.tbimg > tr > td.t > a')
times = Soup.select('table.tbimg > tr > td.t > span.fl')
prices = Soup.select('td.tc > b.pri')


i=0
for title,time,price in zip(titles,times,prices):
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
        print(data)

print(i)

