from bs4 import BeautifulSoup
import requests
import time

page = 0
house_list = []
list_limit = 300
file = open('info_list.txt', 'w')

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Content-Type': 'text/html; charset=utf-8'
}

# function to get a house detail page's info
def get_info(url):
    info_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(info_data.text, 'lxml')
    title = soup.select('div.pho_info > h4 > em')[0].get_text()
    address = soup.select('.pr5')[0].get_text()
    rent = soup.select('.bg_box div.day_l > span')[0].get_text()
    room_photo = soup.select('#curBigImage')[0].get('src')
    lorder_photo = soup.select('.bg_box .member_pic img')[0].get('src')
    lorder_name = soup.select('.bg_box a.lorder_name')[0].get_text()
    lorder_gender = u'女' if soup.select('.member_ico1') else u'男'
    print(u'{}: 标题: {}, 地址: {}, 每晚租金: {}元, 房屋照片: {}, 房东名字: {}, 房东头像: {}, 房东性别: {}'.format
          (len(house_list), title, address, rent, room_photo, lorder_name, lorder_photo, lorder_gender))
    file.write(u'{}: 标题: {}, 地址: {}, 每晚租金: {}元, 房屋照片: {}, 房东名字: {}, 房东头像: {}, 房东性别: {} \n----------\n'.format
          (len(house_list), title, address, rent, room_photo, lorder_name, lorder_photo, lorder_gender))
    time.sleep(1)

while(len(house_list) < list_limit):
    page += 1
    page_url = 'http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(page)
    page_data = requests.get(page_url,headers=headers)
    soup = BeautifulSoup(page_data.text, 'lxml')
    info_lists = soup.select('#page_list .pic_list li')
    for info_list in info_lists:
        info_url = info_list.select('.resule_img_a')[0].get('href')
        if len(house_list) < list_limit:
            house_list.append(info_url)
            get_info(info_url)
        else:
            break