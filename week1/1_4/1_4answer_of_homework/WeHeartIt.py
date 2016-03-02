import requests
from bs4 import BeautifulSoup
import urllib.request

# 'http://weheartit.com/inspirations/beach?page=8' full url

base_url = 'http://weheartit.com/inspirations/beach?page='
path = '/Users/Hou/Desktop/aaa/'
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
}

proxies = {"http": "http://121.69.29.162:8118"}

# 此网站会有针对 ip 的反爬取，可以采用代理的方式

def get_image_url(num):
    img_urls = []
    for page_num in range(1,num+1):
        full_url = base_url + str(page_num)
        wb_data  = requests.get(full_url,proxies=proxies)
        soup = BeautifulSoup(wb_data.text,'lxml')
        imgs = soup.select('img.entry_thumbnail')

        for i in imgs :
            img_urls.append(i.get('src'))

    print((len(img_urls)),'images shall be downloaded!')
    return img_urls

# get_image_url(1)

# 'http://data.whicdn.com/images/224263340/superthumb.jpg'
def dl_image(url):
    urllib.request.urlretrieve(url,path + url.split('/')[-2] + url.split('/')[-1])
    print('Done')

#
for url in get_image_url(10):
    dl_image(url)
