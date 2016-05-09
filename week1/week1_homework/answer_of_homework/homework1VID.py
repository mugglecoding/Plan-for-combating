from bs4 import BeautifulSoup
import requests
import time

url = 'http://bj.58.com/pingbandiannao/24604629984324x.shtml'

wb_data = requests.get(url)
soup = BeautifulSoup(wb_data.text,'lxml')

def get_links_from(who_sells):
    urls = []
    list_view = 'http://bj.58.com/pbdn/{}/pn2/'.format(str(who_sells))
    wb_data = requests.get(list_view)
    soup = BeautifulSoup(wb_data.text,'lxml')
    for link in soup.select('td.t a.t'):
        urls.append(link.get('href').split('?')[0])
    return urls


def get_views_from(url):
    id = url.split('/')[-1].strip('x.shtml')
    api = 'http://jst1.58.com/counter?infoid={}'.format(id)
    # 这个是找到了58的查询接口，不了解接口可以参照一下新浪微博接口的介绍
    # 浏览量的抓取做了反爬虫，因此加上header信息，不然返回为空
    headers = {'User-Agent':r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
               'Cookie':r'id58=c5/ns1ct99sKkWWeFSQCAg==; city=bj; 58home=bj; ipcity=yiwu%7C%u4E49%u4E4C%7C0; als=0; myfeet_tooltip=end; bj58_id58s="NTZBZ1Mrd3JmSDdENzQ4NA=="; sessionid=021b1d13-b32e-407d-a76f-924ec040579e; bangbigtip2=1; 58tj_uuid=0ed4f4ba-f709-4c42-8972-77708fcfc553; new_session=0; new_uv=1; utm_source=; spm=; init_refer=; final_history={}; bj58_new_session=0; bj58_init_refer=""; bj58_new_uv=1'.format(str(infoid)),
               'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Host':'jst1.58.com',
               'Referer':r'http://bj.58.com/pingbandiannao/{}x.shtml'.format(str(infoid))
               }
    js = requests.get(api,headers = headers)
    #js = requests.get(api)
    views = js.text.split('=')[-1]
    return views
    # print(views)


def get_item_info(who_sells=0):

    urls = get_links_from(who_sells)
    for url in urls:

        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.text,'lxml')
        data = {
            'title':soup.title.text,
            'price':soup.select('.price')[0].text,
            'area' :list(soup.select('.c_25d')[0].stripped_strings) if soup.find_all('span','c_25d') else None,
            'date' :soup.select('.time')[0].text,
            'cate' :'个人' if who_sells == 0 else '商家',
            # 'views':get_views_from(url)
        }
        print(data)

# get_item_info(url)

# get_links_from(1)

get_item_info()