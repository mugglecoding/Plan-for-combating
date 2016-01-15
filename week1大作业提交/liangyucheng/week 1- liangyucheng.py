__author__ = 'kennyliang'
import requests
from bs4 import BeautifulSoup
import time
import re
import urllib.request
import xlsxwriter

# 初始化一个excel表格，作为存储
filename = "homework1.xlsx"
workBook = xlsxwriter.Workbook(filename)
ws1 = workBook.add_worksheet()

ws1.write(0, 0, "title")
ws1.write(0, 1, "time")
ws1.write(0, 2, "price")
ws1.write(0, 3, "visit")
ws1.write(0, 4, "type")
ws1.write(0, 5, "level")
ws1.write(0, 6, "area")

url_s = "http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36"
}

page = requests.get(url_s, header)
soup = BeautifulSoup(page.text, 'lxml')
url_lv2 = soup.select("tr > td.t > a.t")  # 获取二级链接

page.close()

# 初始化
url_new = []

for i in url_lv2:
    url_1 = i.get("href")
    url_new.append(url_1)

for i in range(len(url_new)):
    ws1.write(i + 1, 8, url_new[i])
    pages = requests.get(url_new[i], header)
    soup = BeautifulSoup(pages.text, 'lxml')
    # 获得标题
    title = soup.select(" #content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.mainTitle > h1")
    # 获得访问人数
    url_s = 'http://jst1.58.com/counter?infoid=' + url_new[i][-16:-2]
    response = urllib.request.urlopen(url_s)
    jsonString = response.read()
    jsonString = str(jsonString)
    p_visit = re.compile(r'total\=(.*?)\"')
    visit = p_visit.findall(jsonString)
    visit = str(visit)
    # 发帖时间
    posttime = soup.select(" #index_show > ul.mtit_con_left.fl > li.time")
    # 价格
    price = soup.select("#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li:nth-of-type(1) > div.su_con > span")
    # 获得买家类型
    typeofbuyer = soup.select(" p > span.red")
    # 类目
    lv = soup.select("#header > div.breadCrumb.f12 > span:nth-of-type(3) > a")
    # 区域
    area = soup.select("#content > div > div > div.col_sub.sumary > ul > li:nth-of-type(3) > div.su_con > span")
    time.sleep(1)
    pages.close()

    for tit, vis, pt, pri, buyer, level, area1 in zip(title, visit, posttime, price, typeofbuyer, lv, area):
        print(tit.get_text())
        visit
        print(pt.get_text())
        print(pri.get_text())
        buyer = buyer.get_text()
        if "普通商家" in buyer:
            type = "普通商家"
        else:
            type = "个人用户"
        print(level.get_text())
        print(area1.get_text())
        ws1.write(i + 1, 0, tit.get_text())
        ws1.write(i + 1, 1, pt.get_text())
        ws1.write(i + 1, 2, pri.get_text())
        ws1.write(i + 1, 3, visit)
        ws1.write(i + 1, 4, type)
        ws1.write(i + 1, 5, level.get_text())
        ws1.write(i + 1, 6, area1.get_text())

workBook.close()
