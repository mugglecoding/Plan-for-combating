from bs4 import BeautifulSoup

data = []
path = '练习题所需网页/index.html'

with open(path,'r') as f:
    Soup    = BeautifulSoup(f.read(), 'lxml')
    images  = Soup.select('body > div > div > div.col-md-9 > div > div > div > img')
    titles  = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4 > a')
    prices  = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4.pull-right')
    # 星星和reviews都是div下面的2个P标签,而星星的p标签没有class,所以要以:nth-of-type(2)来表示div中的第二个p
    stars   = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p:nth-of-type(2)')
    reviews = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p.pull-right')

for image, title, price, star, review in zip(images, titles, prices, stars, reviews):
    info = {
        'title' : title.get_text(),
        'image' : image.get('src'),
        'price' : price.get_text(),
        # 通过find_all()方法查找全部class_= "glyphicon glyphicon-star"(实心星星)的span标签,返回的是列表,所以通过len()来得到列表中元素个数
        'star'  : len(star.find_all("span",class_= "glyphicon glyphicon-star")),
        # 只要数字,不要review,所以只取' review'前的字符,string[:-8]
        'review': review.get_text()[:-8]

    }
#   将字典装入列表
    data.append(info)

for i in data:
    print(i['title'], i['price'], str(i['star'])+' stars and', str(i['review'])+' reviews','\n----------\n')