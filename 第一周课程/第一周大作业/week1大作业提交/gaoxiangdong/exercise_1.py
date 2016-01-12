from bs4 import BeautifulSoup
import time
import requests
data = []

# 用于模拟手机登录使用
headers = {
       'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4'
}

# 使用 format(str(i)) for i in range(1, 4)获得多个网页
urls = ['http://m.58.com/bj/pbdn/pn{}/?reform=pcfront&PGTID=0d305a36-0000-140a-35f7-6753843b0650&ClickID=2&segment=true'.format(str(i)) for i in range(1, 3)]


# 获得单个商品的基本信息
def get_detail_info(url, detail_info=None):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    titles = soup.select('  div.left_tit > h1')
    release_times = soup.select(' div.date')
    prices = soup.select(' p.attr_price > span ')
    seller_types = soup.select('#personal > span.pcate')
    areas = soup.select('div.location > a')
    if detail_info is None:
        for title,  release_time, price,  seller_type, area, in zip(titles ,  release_times, prices, seller_types, areas, ):
            detail_info = {
                'title': title.get_text(),
                'page_view': get_page_view(url),
                'release_time': release_time.get_text(strip=True),
                'price': price.get_text(),
                'seller_type': seller_type.get_text(),
                'area': area.get_text(),

            }

        return detail_info


# 获取商品的基本信息
# 在list页面获得每个商品的url
# 把url传递给detail_info()获得每个商品的基本信息
def get_list_info(url, data_list= None):

    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    url_details = soup.select(' body > li ')
    time.sleep(2)
    if data_list is None:
        for url_detail in url_details:
            url_str = url_detail.find('a',).get('href')
            url_type = url_str.find('http://m.zhuanzhuan.58.com/')
            # 网址有三种类型，http://m.zhuanzhuan.58.com/ 暂时不获取
            # 其他两种使用detail_info()方法获得数据
            if url_type == -1:
                data.append(get_detail_info(url_str))


# 获得page_view
# 思路：查看网页的源代码，浏览量的值为0 审查元素看到的游览量不为空可判断为该值是通过js获得的
# 点击network 刷新网页，观察哪个url的response 返回的值包含浏览量
# 观察得到http://jst1.58.com/counter?infoid={}
# 接下来就是拼接 url 解析数据
def get_page_view(url):

    # 根据 url 中的entinfo索引值获得 entinfo的值，它的值等于infoid
    entinfo_index = url.find('entinfo')
    infoid = url[entinfo_index+8:entinfo_index+22]
    # 根据infoid 拼接 获得 page_view 需要的url
    page_view_url = 'http://jst1.58.com/counter?infoid={}'.format(infoid)

    # 解析数据
    page_view_data = requests.get(page_view_url,)
    page_view_soup = BeautifulSoup(page_view_data.text,'lxml')

    page_views = page_view_soup.select('p')
    page_view_str = page_views[0].get_text().split(';')[1]
    page_view_index = page_view_str.find('=')
    page_view_length = len(page_view_str)
    page_view = page_view_str[page_view_index+1:page_view_length]
    print('infoid:'+infoid)
    print('浏览量:'+page_view)

    return page_view

# 获取多个网页的数据
for url in urls:
    get_list_info(url)

# 打印获取的数据
for i in data:
    print(i)

print(data.__len__())



