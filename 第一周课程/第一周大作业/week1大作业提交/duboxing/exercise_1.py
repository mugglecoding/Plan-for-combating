import time
from bs4 import BeautifulSoup
import requests


def crawler_58(main_url):
    web_data_main = requests.get(main_url).text  # 解析作业目标页面
    soup_main = BeautifulSoup(web_data_main, 'lxml')
    devide_urls = soup_main.select('a.t')  # 抓每个商品的详情页面所在的标签

    for devide_url in devide_urls:
        devide_url_href = devide_url.get('href')  # 循环提取出每个详情页面的网址
        web_data_devide = requests.get(devide_url_href).text
        soup_devide = BeautifulSoup(web_data_devide, 'lxml')
        project_id = str(soup_devide.select('head > meta:nth-of-type(2)')[0])[-50:-36]  # 提取head标签中含有商品ID的网址并截取商品ID
        js_url = 'http://jst1.58.com/counter?infoid={}'.format(project_id)  # 生成商品浏览量的JS地址
        js_data = requests.get(js_url).text
        soup_js = BeautifulSoup(js_data, 'lxml')
        view_count = str(soup_js)[86:-18]  # 截取商品浏览量
        title = soup_devide.select('div.col_sub.mainTitle > h1')[0].text  # 抓取标题
        date = soup_devide.select('li[title="发布日期"]')[0].text  # 抓取发布日期
        price = soup_devide.select('div.per_ad_left > div.col_sub.sumary > ul > li:nth-of-type(1) > div.su_con > span')[
            0].text  # 抓取价格
        kind = soup_devide.select('div.breadCrumb.f12 > span:nth-of-type(3) > a')[0].text  # 抓取类目
        sellerinfo = soup_devide.select('p[class="c_666"]')  # 筛选出包含商家信息的部分
        if "商家" in str(sellerinfo):  # 判断信息中是否有“商家”二字
            seller_type = "商家"
        else:
            seller_type = "个人"
        areainfo = soup_devide.select('div.per_ad_left > div.col_sub.sumary')  # 抓取商品信息区域的全部内容
        if "区域" in str(areainfo):  # 检测这部分内容中是否有“区域”两个字
            area = ' '.join(soup_devide.select('span.c_25d ')[0].text.split())  # 如果有，则抓取区域信息并删除制表符/t和换行/n
            if len(area) == 0:  # 有些人虽然出现了“区域”两个字但是内容为空，排除这些情况
                area = '无'
        else:
            area = '无'  # 未出现“区域”则无区域信息
        print(
            '商品标题：{},浏览量：{}，发帖时间：{}，价格：{},卖家类型：{}，区域：{}，类目：{}'.format(title, view_count, date, price, seller_type, area,
                                                                      kind))
        time.sleep(2)  # 延时抓取防屏蔽


main_url = 'http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'
crawler_58(main_url)
