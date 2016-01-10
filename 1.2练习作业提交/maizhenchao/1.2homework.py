from bs4 import BeautifulSoup

path = 'D://1.2homework/1.2homework/index.html'
with open(path, 'r') as wb_data:
    soup = BeautifulSoup(wb_data, 'lxml')
    images = soup.select('body > div > div > div.col-md-9 > div > div > div > img')
    titles = soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4 > a')
    prices = soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4.pull-right')
    reviews = soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p.pull-right')
    rates = soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p:nth-of-type(2)')

data = []
for image,title,price,review,rate in zip(images,titles,prices,reviews,rates):
    info ={
        'title': title.get_text(),
        'price': price.get_text(),
        'review': review.get_text()[:-8],
        'image': image.get('src'),
        'rate': len(rate.select('span.glyphicon-star'))
    }
    data.append(info)
print(data)
