from multiprocessing import Pool
from channel_extact import channel_list
import pages_parsing
import pymongo
client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
test = ganji['test']

test.remove({})
test.insert_one({'name': 'gxd01', 'age': '10'})
test.insert_one({'name': 'gxd02', 'age': '20'})
test.insert_one({'name': 'gxd03', 'age': '30'})

# def get_all_links_from (channel):
#     for i in range(1,100):
#         get_links_from(channel,i)


def get_test_from_sheet(test_sheet):
    test_data =[]
    for item in test_sheet.find():
        test_data.append(item)
    return  test_data


def print_test_age(test_data):
    print(test_data['age'])


def print_test_name(test_data):
    print(test_data['name'])

if __name__ == '__main__':
    pool = Pool()
    pool.map(print_test_age, get_test_from_sheet(test))
    pool.map(print_test_name,get_test_from_sheet(test))

