from bs4 import BeautifulSoup
import requests
import pymongo

client = pymongo.MongoClient('localhost',27017)
shouji = client['shouji']
shouji_link = shouji['shouji_link']
shouji_info = shouji['shouji_info']
shouji_info2 = shouji['shouji_info2']
shouji_info1 = shouji['shouji_info1']
shouji_sorted1 = shouji['shouji_sorted1']

# 获取所有二手手机有效的链接
url = ''
shoujilink = []

def get_links(url):
    i = 1
    #http://bj.ganji.com/shouji/o2/
    while True:
        url1 = url+'o'+str(i)+'/'
        wb_data = requests.get(url1)
        soup = BeautifulSoup(wb_data.text,'lxml')

        # while True:
        if soup.find_all('ul','pageLink'):
            itemlinks = soup.select('a.ft-tit')
            for a in itemlinks:
                link = a.get('href')
                if 'zhuanzhuan' in link.split('.'):
                    pass
                elif 'click' in link.split('.'):
                    pass
                else:
                    if link in [a['link'] for a in shouji.shouji_link.find()]:
                        print ('already exists')
                        pass
                    else:
                        print (link)
                        shouji.shouji_link.insert_one({'link':link})
                        # shouji_link.insert_one({'link':link})
            print (shouji.shouji_link.find().count())
            i = i+1
        else:
            pass



print (shouji.shouji_link.find().count())

# 获取每个链接对应的商品 价格,成色信息.
def get_info(url):

    #先要判断该链接是否已经解读过


    if url in [i['link'] for i in shouji_info.find()]:

        pass
    else:

        wb_data = requests.get(url,'utf-8')
        soup = BeautifulSoup(wb_data.text,'lxml')
        # print (soup)
        if soup.find_all('ul','second-det-infor clearfix'):

            price = soup.select('i.f22.fc-orange.f-type')[0].get_text()
            status = soup.select('ul.second-det-infor.clearfix > li')[0].get_text()
            print ('price: ',price,'status: ',status,url)
            shouji_info.insert_one({'price':price,'status':status,'link':url})

        else:
            print ('no status')
            pass


for url in [i['link'] for i in shouji_link.find()]:
      # print (url)
    get_info(url)
    print (shouji.shouji_info.find().count())

# 整理状态表达,统一只用 xx新来表达,整理到数据库 shouji_info1
for i in shouji_info2.find():
    info = i['status'].split(' ') if len(i['status'].split(' '))>9 else None
    if info == None:
        pass
    else:
        info = info[8].split('新')[0]+'新'
        #print({'status':info,'price':i['price']})
        shouji.shouji_info1.insert_one({'status':info,'price':i['price']})


# 求出各个状态下的平均值,并储存在新的数据库 shouji_sorted1 里面,用于之后的排序.
pipeline = [
    {'$group':{'_id':'$status','counts':{'$sum':1}}},

]

for i in shouji_info1.aggregate(pipeline):
    sum = 0
    for a in shouji_info1.find({'status':i['_id']}):
        sum = sum + int(a['price'])
    avg = int(sum/i['counts'])
    shouji_sorted1.insert_one ({'name':i['_id'],'data':[avg],'type':'line'})


# 将shouji_sorted1 按照平均值从小到大排序,并以此产生,用于之后的表格数据.
def sort():
    pipeline=[{'$sort':{'data':1}}]

    for i in shouji_sorted1.aggregate(pipeline):
        yield


# 画出线图
options = {
    'chart'  :{'zoomType':'xy'},
    'title'  :{'text':'二手手机成色对均价影响'},
    'subtitle':{'text':'可视化统计图表'},
    'xAxis'   :{'categories':[i['name'] for i in sort()]},
    'yAxis'   :{'title':{'text':'平均价'}}
     }

series = [i['data'] for i in sort()]


charts.plot(series,options=options,show='inline')