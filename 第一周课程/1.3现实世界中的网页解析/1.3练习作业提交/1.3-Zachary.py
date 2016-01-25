from bs4 import BeautifulSoup
import requests
import time
import re

# ******************** 1.3 课堂模仿练习 ********************
'''
headers = {
    'User-Agent':'',
    'Cookie':''
}
url_saves = ''
url = ''
'''
'''
wb_data = requests.get(url_saves, headers=headers)
wb_data = requests.get(url)
soup = BeautifulSoup(wb_data.text, 'lxml')
#print(soup)

titles = soup.select('div.property_title > a')
images = soup.select('img[width="160"]')
cates  = soup.select('')
#print(titles, images, cates, sep='\n=====')

for title,image,cate in zip(titles,images,cates):
    data = {
        'title':title.get_text(),
        'image':image.get('src'),
        'cate' :list(cate.stripped_strings),
    }
    print(data)
'''
'''
def get_attractions(url, data=None):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    titles = soup.select('')
    images = soup.select('')
    tags   = soup.select('')

    for title,image,tag in zip(titles,images,tags):
        data = {
            'title':title.get_text(),
            'image':image.get('src'),
            'tag' :list(tag.stripped_strings),
        }
        print(data)
#get_attractions(url)

def get_favs(url, data=None):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    titles = soup.select('')
    images = soup.select('')
    tags   = soup.select('')

    if data == None:
        for title,image,tag in zip(titles,images,tags):
            data = {
                'title':title.get_text(),
                'image':image.get('src'),
                'tag' :list(tag.stripped_strings),
            }
            print(data)
#get_favs(url_saves)
'''

# ******************** 1.3 练习作业 ********************
# 抓取小猪短租北京的300个短租房资料
# http://bj.xiaozhu.com/search-duanzufang-p1-0/
# 包括:
# 一,住房信息: 1,标题 2,图片链接 3,房屋地址 4,房屋日租金
# 二,房主信息: 1,性别 2,昵称 3,头像

'''
page_url:
    page1:  http://bj.xiaozhu.com/search-duanzufang-p1-0/
    page2:  http://bj.xiaozhu.com/search-duanzufang-p2-0/
    pageX:  http://bj.xiaozhu.com/search-duanzufang-p{}-0/
    # 共5254个结果,每页24个结果,共219页,取前300个,查询14页

    house_url:  #page_list > ul > li > a.herf / .resule_img_a

info:
    title:      body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > h4 > em
    image:      #curBigImage
    address:    body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > p
    price:      #pricePart > div.day_l > span

    name:       .lorder_name / #floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a
    portrait:   .member_pic img / #floatRightBox > div.js_box.clearfix > div.member_pic > a > img
    sex:        .member_boy_ico / .member_girl_ico

    流程:
    1. 获得房屋信息搜索页面信息 更新页数
    2. 获得租房主页 url
    3. 进入租房主页 并获得信息 更新数量
'''

number = 1
number_limit = 301
page = 1
headers = {
    'Content-Type':'text/html; charset=utf-8',
    'User_Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
}

def get_info(url, headers, data=None):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    title       = soup.select('.pho_info h4 em')[0].get_text()
    image       = soup.select('#curBigImage')[0].get('src')
    address     = soup.select('.con_l .pho_info p')[0].get('title')
    price       = soup.select('#pricePart .day_l span')[0].get_text()
    name        = soup.select('.lorder_name')[0].get_text()
    portrait    = soup.select('.member_pic img')[0].get('src')
    sex         = u'男' if soup.select('.member_boy_ico') else u'女'
    data = {
        'No':number,
        'title':title,
        'image':image,
        'address':address,
        'price':price,
        'name':name,
        'portrait':portrait,
        'sex':sex,
    }
    print(data)
    time.sleep(2)

while number < number_limit:
    url_page = 'http://bj.xiaozhu.com/search-duanzufang-p%s-0/' % page
    wb_data = requests.get(url_page, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    page_info = soup.select('#page_list li')
    for i in range(0,24):
        url_house = page_info[i].select('.resule_img_a')[0].get('href')
        get_info(url_house,headers)
        number += 1
        if number == 301:break
    page += 1

