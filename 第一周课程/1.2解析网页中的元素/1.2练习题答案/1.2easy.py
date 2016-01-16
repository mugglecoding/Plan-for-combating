from bs4 import BeautifulSoup

with open('Desktop/12/index.html', 'r') as wb_data:
    Soup = BeautifulSoup(wb_data, 'lxml')
    # print(wb_data)

    titles = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4 > a')
    images = Soup.select('body > div > div > div.col-md-9 > div > div > div > img')
    reviews = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p.pull-right')
    prices = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4.pull-right')
    stars = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p:nth-of-type(2)')
    # 为了从父节点开始取,此处保留:nth-of-type(2),观察网页,多取几个星星的selector,就发现规律了

# print(titles,images,rates,prices,stars,sep='\n--------\n')

for title, image, review, price, star in zip(titles, images, reviews, prices, stars):
    data = {
        'title': title.get_text(),
        'image': image.get('src'),
        'review': review.get_text(),
        'price': price.get_text(),
        'star': len(star.find_all("span", class_='glyphicon glyphicon-star'))
        # 使用find_all 统计有几处是★的样式,再使用len 计算列表中的元素个数
    }
    print(data)
