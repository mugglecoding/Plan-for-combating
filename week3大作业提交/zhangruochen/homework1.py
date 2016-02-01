
# coding: utf-8

# In[1]:

#一定时间内北京各城区发贴量最多的三大类目


# In[1]:

import pymongo
import charts
from datetime import timedelta,date


# In[2]:

client = pymongo.MongoClient('localhost', 27017)
test = client['test']
homework = test['homework']
homework_output = test['homework_output']

In[18]:

for i in homework.find():
    if (i['area']==[]) or (i['area'] == None):
        area_dist = None
    else:
        area_dist = i['area'][0]
    homework.update_one({'_id':i['_id']},{'$set':{'area_dist':area_dist}})

In[24]:

for i in homework.find():
    frags = i['pub_date'].split('.')
    if len(frags) == 1:
        date = frags[0]
    else:
        date = '%s-%s-%s'%(frags[0],frags[1],frags[2])
    homework.update_one({'_id':i['_id']},{'$set':{'pub_date':date}})


# In[3]:

def get_all_dates(date1,date2):
    the_date = date(int(date1.split('-')[0]),int(date1.split('-')[1]),int(date1.split('-')[2]))
    end_date = date(int(date2.split('-')[0]),int(date2.split('-')[1]),int(date2.split('-')[2]))
    days = timedelta(days=1)
    while the_date <= end_date:
        yield (str(the_date)) 
        the_date += days

# In[4]:

def get_data_within(date1,date2,cates,area_dist):
    data_list = []
    for cate in cates:
        total_post = 0
        for date in get_all_dates(date1,date2):
            a = list(homework.find({'area_dist':area_dist,'cates':cate,'pub_date':date}))
            each_day_post = len(a)
            total_post += each_day_post
#         print(area_dist,cate,total_post)
        data_ori = {
        'name':cate,
        'data':[total_post],
        'type':'column'
    }
        data_list.append(data_ori)
    data_list.sort(key=lambda x:x['data'][0])
    data = data_list[-3:]
    for i in data:
        yield i
#     print(data_list)


# In[5]:

cates=[]
dists=[]
for i in homework.find():
    cates.append(i['cates'])
    dists.append(i['area_dist'])
cates_index = list(set(cates))
dists_index = list(set(dists))
# print(cates_index,dists_index)


# In[6]:
for dist in dists_index:
    series = [i for i in get_data_within('2015-12-21','2016-01-15',cates_index,dist)]
    charts.plot(series, options=dict(title=dict(text='各大区排名前三类目及发帖量'), subtitle=dict(text=dist), yAxis=dict(title=dict(text='发帖量'))))
