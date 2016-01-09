from bs4 import BeautifulSoup
import requests

url = 'http://bj.58.com/pingbandiannao/24617948333885x.shtml'
five8_data = requests.get(url)
soup = BeautifulSoup(five8_data.text,'lxml')

title = soup.title.text
price = soup.select('span.price')
date = soup.select('li.time')
area = soup.select('.c_25d')

def get_links_from(sells):
    urls = []
    list_views = 'http://bj.58.com/pbdn/{}/'.format(str(sells))
    five8_data = requests.get(list_views)
    soup = BeautifulSoup(five8_data.text,'lxml')
    for link in soup.select('td.t a.t'):
        urls.append(link.get('href').split('?')[0])
    return urls
    #print(urls)

def get_views_from(url):
    id = url.split('/')[-1].strip('x.shtml')
    api = 'http://jst1.58.com/counter?infoid={}'.format(id)
    five8_data = requests.get(api)
    views = five8_data.text.split('=')[-1]
    return views
    #print(views)

def get_item_info(sells = 0):
    urls = get_links_from(sells)
    for url in urls:

        five8_data = requests.get(url)
        soup = BeautifulSoup(five8_data.text,'lxml')
        data = {
            'title':title,
            'price':price[0].text,
            'date':date[0].text,
            'area':list(area[0].stripped_strings) if soup.find_all('span','c_25d') else None,
            'cate':'个人' if sells == 0 else '商家',
            'views':get_views_from(url)
        }
        print(data)

get_item_info()

