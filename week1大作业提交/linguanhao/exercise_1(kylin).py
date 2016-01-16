from bs4 import BeautifulSoup
import requests
import re

def get_page_content(url):
    ''' 返回该网页的 html代码 '''

    header = {  #模拟浏览器
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
    }
    page_content = requests.get(url, headers=header)
    return page_content.text

def run_spider(url, file):
    '''
    功能：将要抓取的内容写入到文件中
    参数：
        url： 网页的 url地址
        file：要保存抓取结果的文件
    '''

    page_content = get_page_content(url)
    index_page_soup = BeautifulSoup(page_content, 'lxml')

    index_page_selector = index_page_soup.select('td.t > a.t')
    detail_urls = [each.get('href') for each in index_page_selector] #detail_urls列表里保存的是该页面中所有的物品的连接地址

    for detail_url in detail_urls:
        detail_page_content = get_page_content(detail_url)
        detail_page_soup = BeautifulSoup(detail_page_content, 'lxml')

        title = detail_page_soup.select('div.col_sub.mainTitle > h1')[0].get_text() #获取标题
        if not title:
            continue  #如果该物品没有标题，就不再分析该物品的其他内容，直接分析下一个物品

        page_view_num = get_page_view_number(detail_page_content)    #获取物品的浏览量
        date = detail_page_soup.select('#index_show > ul.mtit_con_left.fl > li.time')[0].get_text()  #获取发帖时间
        price = detail_page_soup.select('div.col_sub.sumary > ul > li:nth-of-type(1) > div.su_con > span')  #获取价格
        if price:
            price = price[0].get_text()
        else:
            price = '未知'

        identify = re.search('商家', detail_page_content) #获取类型：如果该页面中出现了‘商家’二字则判断此人为商家，否则为个人
        if identify:
            identify = '商家'
        else:
            identify = '个人'

        area = detail_page_soup.select('div.su_con > span.c_25d') #获取地址
        if not area:
            area = '未知'
        else:
            area = area[0].get_text().replace('\t','').replace('\r\n','').replace('\n', '')  #格式化地址的格式

        type = detail_page_soup.select('#main > div.col.detailPrimary.mb15 > div > div > div.more-goods > div.more-goods-b > p > a') #获取物品的类目
        if type:
            type =  type[0].get_text()[:-2]
        else:
            type = '未知'


        data = {
            '标题' : title,
            '浏览量' : page_view_num,
            '发帖时间' : date,
            '价格' : price,
            '卖家类型' : identify,
            '区域' : area,
            '类目' : type
        }

        for key in data:  #将字典写入文件中
            file.write(key)
            file.write('\t')
            file.write(data[key])
            file.write('\t')
        file.write('\n')

        print(data)

def get_page_view_number(page_content):
    '''
    功能：获取该帖子的浏览量
    参数：
        page_content: 帖子的html代码
    '''

    #通过获取五个参数来构建新的url地址，该地址中含有帖子的浏览量
    goods_infoid = re.findall('Counter58.infoid=(.*?);', page_content, re.S)[0]
    goods_sid = re.findall('Counter58.sid="(.*?)";', page_content, re.S)[0]
    goods_px = re.findall('Counter58.px="(.*?)";', page_content, re.S)[0]
    goods_lid = re.findall('Counter58.lid="(.*?)";', page_content, re.S)[0]
    goods_cfpath = re.findall('Counter58.cfpath="(.*?)";', page_content, re.S)[0]

    page_view_url = 'http://jst1.58.com/counter?infoid={}&userid=&uname=&sid={}&lid={}&px={}&cfpath={}'.format(goods_infoid, goods_sid, goods_lid, goods_px, goods_cfpath)
    page_view_result = get_page_content(page_view_url)
    page_view_num = page_view_result.split('=')[-1]

    return page_view_num


if __name__ == '__main__':
    file = open('result_1-4.xls','w',encoding='utf-8') #将结果保存在文件result_1-4.xls中，可以用excel打开
    url = 'http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'
    run_spider(url, file)
