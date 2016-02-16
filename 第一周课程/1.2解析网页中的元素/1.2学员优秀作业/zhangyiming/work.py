from bs4 import BeautifulSoup

info = []

with open('index.html','r') as wb_data:
    Soup = BeautifulSoup(wb_data,'lxml')

    titles = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4 > a')
    images = Soup.select('body > div > div > div.col-md-9 > div > div > div > img')
    prices = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4.pull-right')
    reviews = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p.pull-right')
    stars = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p:nth-of-type(2)')

for title, image, price, review, star in zip(titles, images, prices, reviews, stars):
    data = {
        'title': title.get_text(),
        'iamge': image.get('src'),
        'price': price.get_text(),
        'review': review.get_text(),
        'star': len(star.find_all("span", class_="glyphicon glyphicon-star"))
    }

    info.append(data)


for i in info:
    if i['star'] > 3:
        print i['title'],i['price']
