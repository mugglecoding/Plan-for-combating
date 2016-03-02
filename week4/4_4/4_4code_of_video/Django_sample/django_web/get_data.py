
def look_price(date1,date2,cates,with_cate=0):

    options = {
        'title': {'text': '新旧-价格'},
        'xAxis'   : {'categories': ['报废机/尸体','7成新及以下','8成新','9成新','95成新','99成新', '全新']},
        'yAxis'   : {'title': {'text': '价格'}},
    }

    pipeline = [
        {'$match':{'$and':[{'pub_date':{'$gte':date1,'$lte':date2}},
                           {'cates':{'$all':cates}},
                           {'look':{'$nin':['-']}}
                          ]}},
        {'$group':{'_id':'$look','avg_price':{'$avg':'$price'}}},
        {'$sort':{'avg_price':1}}
    ]

    for i in ItemInfo._get_collection().aggregate(pipeline):
        if with_cate == 0:
            yield i['avg_price']
        if with_cate == 1:
            yield i['_id']

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -