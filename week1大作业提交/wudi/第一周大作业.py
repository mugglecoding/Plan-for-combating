from bs4 import BeautifulSoup
import requests
import time

def get_info(url):#获取详细页信息

    print(url)#显示连接 出错好查
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')

    titles = soup.title
    times   = soup.select('li.time')
    Prices  = soup.select('span.price')
    areas   = soup.select('span.c_25d')

    data    = {
                'title':titles.text,#标题
                'time ':times[0].text if soup.select('li.time') else '无日期',#发帖时间
                'Price':Prices[0].text if soup.select('span.price') else None,#价钱
                'area ':''.join(areas[0].text.split())if soup.select('span.c_25d') else None,#区域
               'browse':get_vivews_from(url),#浏览量
                'type ':'商家'if soup.select('ul.vcard li em.medium') else '个人'#卖家类型
    }

    print('标题:{} 卖家类型:{} \n发布日期:{} 价格:{} \n浏览量:{} 地区:{}'
          .format(data['title'],data['type '],data['time '],data['Price'],data['browse'],data['area ']))
    print('++++++++++++++++++++++++++++++++++++++++')
    time.sleep(2)

def get_links(who_sell=0,start=1,end=3):#获取首页地址 每页详细页地址
    for i in range(start,end):
        url = 'http://bj.58.com/pbdn/{}/pn{}'.format(str(who_sell),str(i))#who_sell=0 是个人 1，是商家
        print(url,'****************************************************************************')
        wb_data = requests.get(url)
        soup =  BeautifulSoup(wb_data.text,'lxml')

        links = soup.find_all(name='tr',attrs={'class':False})
        all_link=[]
        for link in links:
            all_link.append(link.select('a.t')[0].get('href'))#再次筛选连接

        for master_link in all_link:
            get_info(master_link)


def get_vivews_from(url):#获取浏览量
    id = url.split('/')[-1].split('x.shtml')[0]
    api = 'http://jst1.58.com/counter?infoid={}'.format(id)
    js  =  requests.get(api)
    views = js.text.split('=')[-1]
    return views


get_links()

'''
商品标题 浏览量 发帖时间 价格 买家类型 区域 类目
'''

