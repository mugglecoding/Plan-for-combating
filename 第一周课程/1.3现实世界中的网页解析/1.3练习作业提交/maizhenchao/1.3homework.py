from bs4 import BeautifulSoup
import requests, time

i = 0
urls = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i)) for i in range(1,100)]
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER',
    'Cookie':'abtest_ABTest4SearchDate=b; OZ_1U_2282=vid=v687f323752f93.0&ctime=1451754946&ltime=1451754932; OZ_1Y_2282=erefer=-&eurl=http%3A//bj.xiaozhu.com/search-duanzufang-p1-0/&etime=1451750179&ctime=1451754946&ltime=1451754932&compid=2282; __utma=29082403.52157338.1451750181.1451750181.1451753701.2; __utmb=29082403.16.10.1451753701; __utmc=29082403; __utmz=29082403.1451750181.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
}

def get_info(url):
    web = requests.get(url,headers=headers)
    time.sleep(1)
    soup = BeautifulSoup(web.text,'lxml')
    title = soup.select('h4 > em')[0].text
    img = soup.select('img[id="curBigImage"]')[0].get('src')
    address = soup.select('span.pr5')[0].text.strip()
    rent = soup.select('.day_l > span')[0].text
    lorder_name = soup.select('.lorder_name')[0].text
    lorder_img = soup.select('.member_pic > a > img')[0].get('src')
    lorder_sex = 'male' if soup.select('.member_boy_ico') else 'female'
    info = 'title:{}, img_link:{}, address:{}, rent:{}, \nlorder_name:{}, lorder_img:{}, lorder_sex:{}'.format(title,img,address,rent,lorder_name,lorder_img,lorder_sex)
    print(info)

for url in urls:
    list_web = requests.get(url,headers=headers)
    time.sleep(1)
    soup = BeautifulSoup(list_web.text,'lxml')
    houses = soup.select('.resule_img_a')
    for house in houses:
        info_link = house.get('href')
        while i < 300:
            get_info(info_link)
            i += 1
    break
