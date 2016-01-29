
from multiprocessing import Pool
from w2_item_url import get_itemurl,item_links4
from w2_channel_extract import category,caturl



# db_urls = [item['url'] for item in item_links3.find()]
# index_urls = [item['url'] for item in detail1.find()]
# x = db_urls
# y = index_urls
# rest_of_urls = x-y

# print (rest_of_urls)

caturl.remove('http://bj.ganji.com/shoujihaoma/')
category.remove('手机号码')


def get_all_links(url):
     get_itemurl(url,url.split('/')[-2])



if __name__ == '__main__':

  for url in caturl:
      get_all_links(url)





