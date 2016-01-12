from bs4 import BeautifulSoup

# ******************** 1.2 课堂模仿练习 ********************
'''
with open('/Users/zsl/Desktop/1.2test/new_index.html', 'r') as wb_data:
    Soup = BeautifulSoup(wb_data, 'lxml')
#    print(Soup)

    images = Soup.select('body > div.main-content > ul > li > img')
    titles = Soup.select('body > div.main-content > ul > li > div.article-info > h3 > a')
    descs  = Soup.select('body > div.main-content > ul > li > div.article-info > p.description')
    rates  = Soup.select('body > div.main-content > ul > li > div.rate > span')
    tags   = Soup.select('body > div.main-content > ul > li > div.article-info > p.meta-info')
#    print(images, titles, tags, descs, rates, sep='\n==========\n')

info = []
for title,desc,rate,tag,image in zip(titles,descs,rates,tags,images):
    data = {
        'title':title.get_text(),
        'desc' :desc.get_text(),
        'rate' :rate.get_text(),
        'tag'  :list(tag.stripped_strings),
        'image':image.get('src')
    }
    info.append(data)
#    print(data)

for i in info:
    if float(i['rate'])>3:
        print(i['title'],i['tag'])
'''

'''
image:          body > div.main-content > ul > li:nth-child(1) > img
title:          body > div.main-content > ul > li:nth-child(1) > div.article-info > h3 > a
description:    body > div.main-content > ul > li:nth-child(1) > div.article-info > p.description
rate:           body > div.main-content > ul > li:nth-child(1) > div.rate > span
cate:           body > div.main-content > ul > li:nth-child(1) > div.article-info > p.meta-info > span:nth-child(1)
'''

# ******************** 1.2 练习作业 ********************
# 解析该本地网页,获取所有商品的标题, 图片地址, 浏览量, 价格, 以及评分.
'''
with open('/Users/zsl/Desktop/1.2homework/index.html', 'r') as wb_data:
    soup = BeautifulSoup(wb_data, 'lxml')
'''

wb_path = '/Users/zsl/Desktop/1.2homework/index.html'
soup = BeautifulSoup(open(wb_path), 'lxml')

titles  = soup.select('div.caption > h4 > a')
images  = soup.select('div.col-md-9 > div > div > div > img')
browses = soup.select('div.ratings > p.pull-right')
prices  = soup.select('div.caption > h4.pull-right')
rates   = soup.select('div.ratings > p:nth-of-type(2)')

star = soup.select('span.glyphicon-star')[0]

for title,image,browse,price,rate in zip(titles,images,browses,prices,rates):
    data = {
        'title' :title.get_text(),
        'image' :image.get('src'),
        'browse':browse.get_text(),
        'price' :price.get_text(),
        'rate'  :list(rate).count(star)
    }
    print(data)

'''
title:  body > div:nth-child(2) > div > div.col-md-9 > div:nth-child(2) > div:nth-child(1) > div > div.caption > h4:nth-child(2) > a
image:  body > div:nth-child(2) > div > div.col-md-9 > div:nth-child(2) > div:nth-child(1) > div > img
browse: body > div:nth-child(2) > div > div.col-md-9 > div:nth-child(2) > div:nth-child(1) > div > div.ratings > p.pull-right
price:  body > div:nth-child(2) > div > div.col-md-9 > div:nth-child(2) > div:nth-child(1) > div > div.caption > h4.pull-right
rate:   body > div:nth-child(2) > div > div.col-md-9 > div:nth-child(2) > div:nth-child(1) > div > div.ratings > p:nth-child(2) > span:nth-child(2)
'''
