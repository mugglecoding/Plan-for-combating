from bs4 import BeautifulSoup
import requests
import time

def get_master_info(master_url):

    wb_data = requests.get(master_url)
    soup = BeautifulSoup(wb_data.text,'lxml')

    titiles = soup.title.text.split('-')[0]
    address = soup.select('span.pr5')
    imgaes  = soup.select('#curBigImage')#图片有很多 以后可以尝试获取全部
    rents    = soup.select('.day_l')
    special_rents = soup.select('.reserve_text ')
    #==================房主信息==============
    names    = soup.select('.lorder_name')
    Genders  = soup.select('.member_pic > div')#div.class的值来判断
    Gender_images = soup.select('.member_pic > a > img')

    data = {
        '标题':titiles,
        '地址':address[0].text.strip('/\r/\n '),
        '图片':imgaes[0].get('src'),
        '租金':list(rents[0].stripped_strings)[1],
        '特价日':''.join(special_rents[0].text.split()) if soup.select('.price_top') else 'None',#去除字符串中间有空格的办法在前面 研究一下午!! 先用split分开在用join组合上
        '房主姓名':names[0].text,
        '房主性别':'男'if Genders[0].get('class')[0] == 'member_ico' else '女',
        '房主头像':Gender_images[0].get('src')
    }
    print('标题:  {}  地址:  {}\n租金:  {}  特价日: {}\n房主昵称:  {} 房主性别:{} \n房主头像:{}\n房屋图片:{} '
          .format(data['标题'],data['地址'],data['租金'],data['特价日'],data['房主姓名'],data['房主性别'],data['房主头像'],data['图片']))
    print('+++++++++++++++++++++++++++++++++++++++++\n'
          '+++++++++++++++++++++++++++++++++++++++++')
'''
标题 title图片连接房屋地址房屋日租金
房主性别房主昵称房主头像
'''
def get_link(strat=1,end=3):
    time.sleep(4)
    for i in range(strat,end):
        url = 'http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i))
        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.text,'lxml')
        links = soup.select('li > a.resule_img_a')
        urls = []
        x = 0
        for link in links:
            urls.append(link.get('href'))
        for master_url in urls:
            x += 1
            get_master_info(master_url)
            print('第{}页第{}个'.format(i,x))
get_link()
