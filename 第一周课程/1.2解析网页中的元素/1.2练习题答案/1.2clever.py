from bs4 import BeautifulSoup
import string

with open('Desktop/12/index.html', 'r') as web_data:
    soup = BeautifulSoup(web_data, 'lxml')
    titles = soup.select(
        'body > div > div > div.col-md-9 > div > div > div > div.caption > h4 > a ')
    images = soup.select(
        'body > div > div > div.col-md-9 > div > div > div > img')
    reviews = soup.select(
        'body > div > div > div.col-md-9 > div > div > div > div.ratings > p.pull-right')
    prices = soup.select(
        'body > div > div > div.col-md-9 > div > div > div > div.caption > h4.pull-right')
    grades_crawler = soup.select(
        'body > div > div > div.col-md-9 > div > div > div > div.ratings > p:nth-of-type(2) > span ')
    # 上一行抓取所有的星星描述
    grades = []  # 设置一个空列表
    while len(grades_crawler) != 0:  # 循环条件长度不为0
        e = grades_crawler[0:5]  # 提取星星描述前五个元素，也就是一个商品的星级
        grades.insert(1, e)  # 把这五个商品星级的列表作为一个元素插入grades列表中
        del grades_crawler[0:5]  # 删除抓取到的描述列表的前五位

for title, image, review, price, grade in zip(titles, images, reviews, prices, grades):
    star = []
    b = str(grade)  # 字符串化列表
    c = b.replace('<span class="glyphicon glyphicon-star"></span>', '★')  # 将描述实五角星的替换为图案
    d = c.replace('<span class="glyphicon glyphicon-star-empty"></span>', '☆')  # 将描述虚五角星的替换为图案
    star.append(d)  # 将转化完的结果逐个插入列表star中
    data = {
        'title': title.get_text(),
        'image': image.get('src'),
        'review': review.get_text(),
        'price': price.get_text(),
        'grade': ''.join(star).replace('[', '').replace(']', '').replace(',', '').replace(' ', '')
    }
    print(data)
