
# coding: utf-8

# In[2]:

#各类目中成色与均价（全，99，95，9，8，7及以下）


# In[1]:

import pymongo
import charts


# In[31]:

client = pymongo.MongoClient('localhost',27017)
test = client['test']
homework = test['homework']
look = test['look']


# In[35]:

for i in homework.find():
    try:
        if i['price'] == '面议':
            int_price = False
        elif u' 元' in i['price']:
            int_price = int(i['price'][:-2])
        elif u'元' in i['price']:
            int_price = int(i['price'][:-1])
        elif i['price'] == '${info.paramsMap.minprice}':
            int_price = False
        else:
            int_price = int(i['price'])
    except ValueError:
        int_price = False
    homework.update_one({'_id':i['_id']},{'$set':{'int_price':int_price}})


# In[50]:

look_list=[]
for i in homework.find():
    look_list.append(i['look'])
look_index_org = set(look_list)
look_index_org.discard('-')
look_index_org.discard('${info.paramsMap.oldlevel}')
look_index_org.discard('报废机/尸体')
look_index = list(look_index_org)
look_index.sort()
look_index.remove('9成新')
look_index.insert(2,'9成新')
print(look_index)


# In[51]:

counts=[]
for index in look_index:
    counts.append(look_list.count(index))
print(counts)


# In[5]:

cates_list = []
for i in homework.find():
    cates_list.append(i['cates'])
cates_index = set(cates_list)
print(cates_index)


# In[74]:

def get_all_price(cates):
    avg_list=[]
    for look in look_index:
        price_list = []
        for i in homework.find(({'cates':cates,'look':look})):
            if i['int_price'] != False:
                price_list.append(i['int_price'])
            else:
                pass
        count = float(len(price_list))
        sum = 0
        for i in price_list:
            sum += i
        try:
            avg = sum/count
            avg_list.append(avg)           
            data = {
                'name':'均价',
                'data':avg_list,
                'type':'line'
                }
        except ZeroDivisionError:
            pass
    yield data


# In[77]:

for cates in cates_index:
    options={
    'chart' : {'zoomType':'xy'},
    'title' : {'text': '二手%s成色对应的平均价格'%cates},
    'xAxis' : {'categories': [i for i in look_index]},
    'yAxis' : {'title': {'text': '价格'}}
    }
    series = [i for i in get_all_price(cates)]
    charts.plot(series, options=options)


# In[68]:

def get_details(cates):
    for look in look_index:
        for i in homework.find(({'cates':cates,'look':look})):
            print(i)

