
# coding: utf-8

# In[1]:

import pymongo,charts


# In[2]:

client = pymongo.MongoClient('localhost',27017)
ganji = client['ganji']
the_sample2 = ganji['the_sample2']


# In[3]:

def get_avg(cates):
    pipeline = [
        {'$match':{'$and':[{'cates':cates},
                  {'look':{'$nin':['-']}}
                   ]}},
        {'$group':{'_id':'$look','avg':{'$avg':'$price'}}},
        {'$sort':{'avg':-1}}


    ]

    for x in the_sample2.aggregate(pipeline):
        yield x['avg']


# In[4]:

data = [i for i in get_avg('北京二手手机')]
options = {
    'title':{'text':'新旧-价格'},
    'xAxis':{'categories':['95成新', '全新', '99成新', '9成新', '8成新', '7成新及以下', '报废机/尸体']},
    'yAxis':{'title':{'text':'价格'}}
}
charts.plot(data,show='inline',options=options)


# In[ ]:



