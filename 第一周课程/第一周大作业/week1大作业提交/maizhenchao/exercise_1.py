from bs4 import BeautifulSoup
import requests, time

url = 'http://bj.58.com/pbdn/?PGTID=0d100000-0000-1121-f41b-137aeef068b7&ClickID=6'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER',
    'Cookie':'ipcity=gz%7C%u5E7F%u5DDE; userid360_xml=82476BBB69A134FD8AB0F237963D72D6; time_create=1454513284375; myfeet_tooltip=end; f=n; id58=05dvOVWUo55swV0vG0n+Ag==; tj_ershoubiz=true; __ag_cm_=1439745474012; __utma=253535702.1351588507.1436196927.1439745423.1439745442.4; __utmz=253535702.1439745442.4.4.utmcsr=market|utmccn=(not%20set)|utmcmd=(not%20set); ag_fid=AbdJAU3SPnEhrNdF; cookieuid=13e1d86b-59e4-4301-9a53-2ee83768f53d; mcity=gz; mcityName=%E5%B9%BF%E5%B7%9E; nearCity=%5B%7B%22city%22%3A%22gz%22%2C%22cityName%22%3A%22%E5%B9%BF%E5%B7%9E%22%7D%5D; 58home=gz; als=0; bj58_id58s="WWx2aFExOEJYMVpLMjUyMg=="; sessionid=f2271f7f-0f4e-43a2-bd48-d02d37c962e1; f=n; ipcity=gz%7C%u5E7F%u5DDE; myfeet_tooltip=end; bdshare_firstime=1451921623886; bj58_new_session=0; bj58_init_refer=""; bj58_new_uv=1; 58tj_uuid=2be7dad9-164f-4d81-8a23-ad5e18d25ac1; new_session=0; init_refer=; new_uv=5; final_history=24565786083005%2C24296408775483'
}

def get_info(url):
    web = requests.get(url, headers=headers)
    time.sleep(2)
    soup = BeautifulSoup(web.text, 'lxml')
    title = soup.select('h1')[0].text
    date = soup.select('.time')[0].text
    price = soup.select('.price')[0].text
    belong = soup.select('span.crb_i')[1].text
    seller_type = '个人' if soup.select('ul.userinfo') else '商家'

    areas = soup.select('span.c_25d')
    if areas == []:
        area = '北京'
    else:
        area = ' '.join(areas[0].get_text().split())

    info_id = url[url.find('info=')+len('info='):url.find('info=')+len('info=')+14]
    js_link = 'http://jst1.58.com/counter?infoid={}'.format(info_id)
    js = requests.get(js_link)
    view = BeautifulSoup(js.text,'lxml').select('p')[0].text.split('=')[-1]

    data = {'商品标题':title,'浏览量':view,'发帖时间':date,'价格':price,'卖家类型':seller_type,'区域':area,'类目':belong}
    print(data)


list_web = requests.get(url,headers=headers)
soup = BeautifulSoup(list_web.text,'lxml')
crawl_lists = soup.select('tr > td.img > a')
for crawl_list in crawl_lists:
    info_url = crawl_list.get('href')
    get_info(info_url)


