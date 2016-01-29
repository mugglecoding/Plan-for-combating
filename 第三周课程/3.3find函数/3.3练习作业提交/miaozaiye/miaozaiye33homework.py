import pymongo
import charts
from datetime import timedelta,date

client = pymongo.MongoClient('localhost',27017)
ganji = client['ganji']
item_info1 = ganji['item_info1']

#简化区域为大区域
for i in item_info1.find():
    a = i['area']
    if a == None:
        pass
    elif len(a)>=1:
        area = a[0]
        #print (a)
        print (area)
        item_info1.update_one({'_id':i['_id']},{'$set':{'area':area}})
    else:
        pass

#统一时间格式为 yy.mm.dd
for i in item_info1.find():
    frags = i['pub_date'].split('-')
    #print (frags)
    if len(frags)>1:
        date = frags[0]+'.'+frags[1]+'.'+frags[2]
        print (date)
        item_info1.update_one({'_id':i['_id']},{'$set':{'pub_date':date}})

#简化品类
for i in item_info1.find():
    cate = i['cates'][2]
    item_info1.update_one({'_id':i['_id']},{'$set':{'cates':cate}})

#数出一段时间包含多少天
#将日期字符输入，转化成为机器识别的日期类型，从起始日期开始，每一天生成一个当天日期，知道日期等于结束日期。

def get_all_dates(date1,date2):
    the_date = date(int(date1.split('.')[0]),int(date1.split('.')[1]),int(date1.split('.')[2]))
    end_date = date(int(date2.split('.')[0]),int(date2.split('.')[1]),int(date2.split('.')[2]))
    days = timedelta(days = 1)
    
    while the_date <= end_date:
        yield (the_date.strftime('%Y.%m.%d'))
        the_date +=days

#数出指定时间段内，指定区域指定品类，发了多少帖
def count_times(date1,date2,areas,cates):
    for area in areas:
        posts = []
        for i in get_all_dates(date1,date2):
            times1 = 0
            for a in list(item_info1.find({'pub_date':i,'area':area})):
                #print (a)
                times = 0
                for cate in cates:
                    if a['cates'] == cate:
                        times = times +1
                    else:
                        pass
                times1 = times1 + times
            posts.append(times1)
        data = {
            'name':area,
            'data':posts,
            'type':'line'
        }
        #print (data)
        yield data    

# 利用Hightchart画出图来
options = {
    'chart'  :{'zoomType':'xy'},
    'title'  :{'text':'发帖量统计'},
    'subtitle':{'text':'可视化统计图表'},
    'xAxis'   :{'categories':[i for i in get_all_dates('2015.12.20','2015.12.30')]},
    'yAxis'   :{'title':{'text':'数量'}}
     }

series = [{'name': '朝阳', 'data': [71, 61, 79, 67, 65, 67, 75, 89, 115, 87, 83], 'type': 'line'},
{'name': '西城', 'data': [25, 15, 9, 15, 14, 13, 25, 12, 11, 18, 12], 'type': 'line'},
{'name': '海淀', 'data': [49, 48, 28, 31, 40, 33, 48, 48, 56, 75, 51], 'type': 'line'}]


charts.plot(series,options=options,show='inline')




