import pymongo
import charts
from datetime import timedelta,date

client = pymongo.MongoClient('localhost',27017)
ganji = client['ganji']
item_info1 = ganji['item_info1']

def get_area_data(area):
    pipeline = [
        {'$match':{'area':area}},
        {'$group':{'_id':'$cates','counts':{'$sum':1}}},
        {'$sort':{'counts':-1}},
        {'$limit':4}
    ]

    for i in item_info1.aggregate(pipeline):
        data = {
            'name':i['_id'],
            'data':[i['counts']],
            'type':'column'
        }
        yield data

series = [data for data in get_area_data('朝阳')]
charts.plot(series,show ='inline',options = dict(title = dict(text ='北京二手交易信息')))