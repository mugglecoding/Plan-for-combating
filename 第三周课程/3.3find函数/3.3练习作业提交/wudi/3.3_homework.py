import pymongo,charts
from string  import punctuation
from datetime import timedelta,date

#------------------------------------------------------------
client = pymongo.MongoClient('localhost',27017)
ganji = client['ganji']
the_sample2 = ganji['the_sample2']
#------------------------------------------------------------

def get_time(day1,day2):                            #获取日期
    start_date = date(int(day1.split('.')[0]),int(day1.split('.')[1]),int(day1.split('.')[2]))
    end_date = date(int(day2.split('.')[0]),int(day2.split('.')[1]),int(day2.split('.')[2]))
    days = timedelta(days=1)
    while start_date <= end_date:                    #条件判断 知道开始日期大于结束日期 停止循环
         yield (start_date.strftime('%Y-%m-%d'))    #格式很关键 影响到后面[mongodb.find   $in] 一个键值对应多条件关系时候 时间格式必须是2016-01-01 '-'是关键 查了半天错 出在这儿了
         start_date = start_date + days             #关键点   strat_date加一天后  返回上一层 促使继续循环


def get_all_info(day1,day2,cates,types='line'):     #主函数  包含获取日期 通过日期 + 类型 统计出某一天某一个类目发帖次数
    for cate in cates:                              #从类目列表获取类目

        count_data = []                             #生成类目的次数列表

        for day in get_time(day1,day2):             #循环天数  取得某一天的值
            count_all = []                          #创建所有类目列表
            for all_date in the_sample2.find({'pub_date':day},{'_id':0,'cates':1,'pub_date':1}):    #根据某一天获得当天所有数据条目
                count_all.append(all_date['cates'][2])      #取得所有数据类目 归入到类目列表里

            count_data.append(count_all.count(cate))        #用类目列表统计类目出现次数   求出 某一天某一个类目发帖次数


        data ={
                    'name':cate,                            #根据第一层类目循环获取类目
                    'data':count_data,                      #从次数列表获取
                    'types':types,                          #图表类型 默认是line

            }

        yield data                  #返回data
#--------------------------------------------------------------------#
options = {
    'chart'  : {'zoomType':'xy'},
    'title'  : {'text':'发帖量统计'},
    'subtitle':{'text':'可视化统计图表'},
    'xAxis'  : {'categories':[i for i in get_time('2016.01.01','2016.01.07')]},
    'yAxis'  : {'title':{'text':'数量'}}
}
series = [i for i in get_all_info('2016.01.01','2016.01.07',['北京二手手机','北京二手台式机/配件','北京二手笔记本'])]
charts.plot(series,options=options,show='inline')
#===================================================================#

# for循环用多了,头疼  一层层认真检查 以免乱了
# 作业总结 1.貌似mongodb数据库查询中 $in条件后面 日期格式 必须是 2016-01-01这种 换成2016.01.01有的能查到有的查不到
#          不知道别人是怎么弄的 我是在这儿卡了半天
#          2.注意chart  series = [{'name'= xxx,'data'=[x,x,x,x],'type'=type}]这个格式
#          注意在函数中我们生成的data 不用加[] 后期列表推导式[x for x in get_all_info]会自动生成[] 这个只能怪自己没认真检查
