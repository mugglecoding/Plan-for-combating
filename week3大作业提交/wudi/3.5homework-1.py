
# coding: utf-8

# In[1]:

import pymongo,time,charts


# In[2]:

client = pymongo.MongoClient('localhost',27017)
ganji = client['ganji']
the_sample2 = ganji['the_sample2']


# In[49]:

def get_area():
    areas = []
    for item in the_sample2.find():
        areas.append(item['area'][0])
    return list(set(areas))


def get_data(date1,date2,area):
    pipeline = [
        {'$match':{'$and':[{'area':{'$all':area}},{'pub_date':{'$gte':date1,'$lte':date2}}]}},
        {'$group':{'_id':{'$slice':['$cates',2,1]},'counts':{'$sum':1}}},
        {'$sort':{'counts':-1}},
        {'$limit':3}
        ]

    
    for x in the_sample2.aggregate(pipeline):
        data ={
            'name':x['_id'][0],
            'data':[x['counts']],
            'type':'column'#圆柱图

        }
        
        yield data



# In[50]:


series = [x for x in get_data('2015.12.15','2016.1.15',['西单'])]
options = {
    'chart'  : {'zoomType':'xy'},
    'title'  : {'text':'发帖量统计'},
    'subtitle':{'text':'可视化统计图表'},
    'yAxis'  : {'title':{'text':'数量'}},
    
}

charts.plot(series,options=options,show='inline')


# In[ ]:



