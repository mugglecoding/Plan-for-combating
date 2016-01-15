#encoding:utf-8
from bs4 import BeautifulSoup
import requests
import time

#以下函数定义起始页的网页列表的获取方法
def get_url_lists(starturl):
    start_web = requests.get(starturl)
    soup = BeautifulSoup(start_web.text,'lxml')
    webs = soup.select('td.t > a.t')
    url_lists = [web.get('href') for web in webs]
    return url_lists

#以下函数定义从列表中的网页中获取内容的方法
def get_web_content(url):
    #下面开始处理页面内容
    web_content = requests.get(url)
    time.sleep(3)
    soup = BeautifulSoup(web_content.text,'lxml')
    titles = soup.select('h1')
    publish_times = soup.select('li.time')
    prices = soup.select('div.su_con > span')
    sale_types = soup.select('div.num_tan_text > span:nth-of-type(1)') #这里要带上span标签的顺序，nth-of-type(1)是第一个标签！
    districts = soup.select('span.c_25d > a')
    categorys = soup.select('span:nth-of-type(3) > a')
    for title,publish_time,price,sale_type,district,category in zip(titles,publish_times,prices,sale_types,districts,categorys):
        #先处理一个js的浏览量问题:
        url_split = url.split('&')
        url_id = url_split[-1][8:-2]
        browse_url='http://jst1.58.com/counter?infoid='+str(url_id)
        browse_content = requests.get(browse_url)
        soup1 = BeautifulSoup(browse_content.text,'lxml')
        browse_nums = str(soup1.p)
        browse_nums_list = browse_nums.split('.')
        browse_num = browse_nums_list[-1][6:-4]
        #下面判断商家和个人的类型
        if(len(sale_type.get_text())==11):
            sale_type='商家'
        else:
            sale_type='个人'
        web_contents = {
            '商品标题':title.get_text(),
            '浏览量':browse_num,
            '发帖时间':publish_time.get_text(),
            '价格' : price.get_text(),
            '卖家类型' : sale_type,
            '区域' : district.get_text(),
            '类目' : category.get_text()
        }
        print(web_contents)

#以下函数循环执行获取目标网页内容
def urls_loop_get(urls):
    for url in urls:
        get_web_content(url)

if __name__=="__main__":
    url = "http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6"
    urls=get_url_lists(url)
    urls_loop_get(urls)