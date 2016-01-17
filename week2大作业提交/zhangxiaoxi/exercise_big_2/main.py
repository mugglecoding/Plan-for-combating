import pymongo
from multiprocessing import Pool
from getfenlei import getFenlei
from getitem import getPageItems
from getpage import getPage
client =pymongo.MongoClient('localhost',27017)
walden=client['ganjiwang']
url_list=walden['url_list']
def get_page_from_fenlei():
    fenleis=getFenlei()
    for fenlei in fenleis:
        getPage(fenlei)

if __name__ == "__main__":
    get_page_from_fenlei()
    pool=Pool()
    pool.map(getPageItems,url_list.find({}, {'url' : 1}))