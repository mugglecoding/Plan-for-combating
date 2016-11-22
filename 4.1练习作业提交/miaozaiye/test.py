import pymongo

client = pymongo.MongoClient('localhost',27017)

ganji = client['ganji']
item_info1 = ganji['item_info1']

for item in item_info1.find().limit(100):
    print (item)


'''
{'_id': ObjectId('5698f528a98063dbe5e91caa'), 'cates': '北京二手家电', 'area': '海淀', 'url': 'http://bj.58.com/jiadian/24494100687030x.shtml', 'pub_date': '2015.12.29', 'price': '1300 元', 'look': '-', 'title': '【图】个人转让西门子带烘干功能滚筒洗衣机 - 海淀知春路二手家电 - 北京58同城'}
{'_id': ObjectId('5698f528a98063dbe4e91cab'), 'cates': '北京二手家电', 'area': '朝阳', 'url': 'http://bj.58.com/jiadian/24636743250110x.shtml', 'pub_date': '2016.01.14', 'price': '600 元', 'look': '-', 'title': '腾房转套时尚床，沙发，衣柜, 一级节能冰箱 滚筒洗衣机 海尔电热水器,液晶电视 - 朝阳太阳宫二手家电 - 北京58同城'}

'''