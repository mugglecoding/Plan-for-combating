from bs4 import BeautifulSoup

data = []
<<<<<<< HEAD:第一周课程/1.2解析网页中的元素/1.2课程案例源码/2_web_parse.py
path = 'web/new_index.html'
=======
path = './web/new_index.html'
>>>>>>> mugglecoding/master:week1/1_2/1_2code_of_video/2_web_parse.py

with open(path, 'r') as f:
    Soup = BeautifulSoup(f.read(), 'lxml')
    titles = Soup.select('ul > li > div.article-info > h3 > a')
    pics = Soup.select('ul > li > img')
    descs = Soup.select('ul > li > div.article-info > p.description')
    rates = Soup.select('ul > li > div.rate > span')
    cates = Soup.select('ul > li > div.article-info > p.meta-info')

for title, pic, desc, rate, cate in zip(titles, pics, descs, rates, cates):
    info = {
        'title': title.get_text(),
        'pic': pic.get('src'),
        'descs': desc.get_text(),
        'rate': rate.get_text(),
        'cate': list(cate.stripped_strings)
    }
    data.append(info)

for i in data:
    if float(i['rate']) > 3:
        print(i['title'], i['cate'])
