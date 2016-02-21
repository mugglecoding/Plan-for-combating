from bs4 import BeautifulSoup
import requests

url = 'http://bj.xiaozhu.com/fangzi/1508951935.html'
wb_data = requests.get(url)
soup = BeautifulSoup(wb_data.text,'lxml')

# 因为是单页面，使用 select 方法获得的元素又是一个列表，那么列表中的第一个元素且也是唯一一个元素即是我们要找的信息 用 “[0]” 索引将其取出
# 后在对其使用处理的方法，因为 beautifulsoup 的些筛选方法并不能针对列表类型的元素使用 ;)


title = soup.select('div.pho_info > h4')[0].text
address = soup.select('div.pho_info > p')[0].get('title') # 和 get('href') 同理，他们都是标签的一个属性而已，我们只需要的到这个属性的内容即可
price = soup.select('div.day_l > span')[0].text
pic = soup.select('#curBigImage')[0].get('src')

host_name = soup.select('a.lorder_name')[0].text
host_gender = soup.select('div.member_pic > div')[0].get('class')[0]

# 请在此处打印并观察结果
print(title)
print(address)
print(price)
print(pic)

print(host_name)
print(host_gender)

# 根据结果观察不同性别会用不同的图标样式（class），设计一个函数进行转换
def print_gender(class_name):
    if class_name == 'member_ico1':
        return '女'
    if class_name == 'member_ico':
        return '男'


data = {
    'title':title,
    'address':address,
    'price':price,
    'pic':pic,
    'host_name':host_name,
    'host_gender':print_gender(host_gender)

}

print(data)