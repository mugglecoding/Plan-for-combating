from bs4 import BeautifulSoup
data = []
path = "index.html"


with open(path,'r') as f:

    Soup   = BeautifulSoup(f.read(),'lxml')

    titles = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4 > a')
    pics   = Soup.select('body > div > div > div.col-md-9 > div > div > div > img')
    views  = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p.pull-right')
    prices = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4.pull-right')
    rates  = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p:nth-of-type(2)')
'''
body > div:nth-child(2) > div > div.col-md-9 > div:nth-child(2) > div:nth-child(1) > div > div.caption > h4:nth-child(2) > a
body > div:nth-child(2) > div > div.col-md-9 > div:nth-child(2) > div:nth-child(1) > div > img
body > div:nth-child(2) > div > div.col-md-9 > div:nth-child(2) > div:nth-child(1) > div > div.ratings > p.pull-right
body > div:nth-child(2) > div > div.col-md-9 > div:nth-child(2) > div:nth-child(1) > div > div.caption > h4.pull-right
body > div:nth-child(2) > div > div.col-md-9 > div:nth-child(2) > div:nth-child(1) > div > div.ratings > p:nth-child(2) > span:nth-child(2)

        'cate' : list(cate.stripped_strings)

'''
for title,pic,view,price,rate in zip(titles,pics,views,prices,rates):
    info = {
        'title': title.get_text(),
        'pic'  : pic.get('src'),
        'view': view.get_text().encode().replace(" reviews",""),
        'price' : price.get_text(),
        'rate' : len(rate.find_all("span",class_='glyphicon glyphicon-star'))
    }
    data.append(info)

for i in data:
    print(i['title'].encode(),i['pic'],i['view'],i['price'],i['rate'])
