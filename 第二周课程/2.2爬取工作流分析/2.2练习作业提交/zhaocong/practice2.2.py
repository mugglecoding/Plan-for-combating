from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017)  # 建立MongoDB连接
data_mobile_num = client['data_mobile_num']  # 建立名为data_mobile_num数据库传递给data_mobile_num
mobile_num_url = data_mobile_num['mobile_num_url']  # 建立名为mobile_num_url数据表传递给mobile_num_url,存储链接
mobile_num_info = data_mobile_num['mobile_num_info']  # 建立名为mobile_num_info数据表传递给mobile_num_info,存储详细信息

top_url = 'http://tj.58.com/shoujihao/0/'


# spider2 爬取商品页面信息
def parse_info(url):
    web_data = requests.get(url)

    soup = BeautifulSoup(web_data.text, 'lxml')
    no_longer_exist = '404' in soup.find('script', type="text/javascript").get('src').split('/')  # 用来确认是否页面为404
    if no_longer_exist:
        pass
    else:
        title = soup.select('h1')[0].text
        time = soup.select('li.time')[0].text
        price = soup.select('span.price.c_f50')[0].text
        area = list(soup.select('.col_sub.sumary ul.suUl li .su_con a')[0].stripped_strings) if soup.find_all('div',
                                                                                                              'su_tit',
                                                                                                              text='区域：') else None  # 根据su_tit的文本值是否包含'区域：'来判断是否包含区域标签
        mobile_num_info.insert_one({'title': title, 'time': time, 'price': price, 'area': area})


# spider1 爬取搜索页面内所有链接和标题
def get_link_from(url):
    web_data = requests.get(top_url)
    soup = BeautifulSoup(web_data.text, 'lxml')
    titles = soup.select('strong.number')
    urls = soup.select('ul li a.t')
    for title, url in zip(titles, urls):
        data = {
            'title': title.text,
            'url': url.get('href')

        }
    mobile_num_url.insert_one(data)

# get_link_from(top_url)
# url = 'http://tj.58.com/shoujihao/24331821468987x.shtml?psid=119798905190418575603948847&entinfo=24331821468987_0&iuType=p_0&PGTID=0d3000f1-0001-2d55-60e6-4e9aaca39089&ClickID=1'
# parse_info(url)
