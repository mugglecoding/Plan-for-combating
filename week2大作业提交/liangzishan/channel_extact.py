from bs4 import BeautifulSoup
import requests
import pymongo
import time

client   = pymongo.MongoClient('localhost', 27017)
local_db = client['local_db']
w2_chnlUrl_col  = local_db['w2_chnlUrl_col']
w2_itmUrl_col   = local_db['w2_itmUrl_col']
w2_itmInfo_col  = local_db['w2_itmInfo_col']

index_url = 'http://bj.ganji.com/wu/'
host_url  = 'http://bj.ganji.com'
headers = {
    'Content-Type': 'text/html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Cookie': 'citydomain=bj; ganji_xuuid=eea59d9c-8b6b-4197-8bcb-e18db2236213.1452772376566; ganji_uuid=2488988877099655998455; GANJISESSID=4bcb39256320bd9d69cf4010fe25cf66; hotPriceTip=1; __utma=32156897.262518560.1452570775.1452790802.1452881661.4; __utmb=32156897.11.10.1452881661; __utmc=32156897; __utmz=32156897.1452790802.3.2.utmcsr=bj.ganji.com|utmccn=(referral)|utmcmd=referral|utmcct=/wu/; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A71596067824%7D',
}

def get_soup(url, headers):
    wb_data = requests.get(url, headers=headers)
    wb_data.encoding = 'utf-8'                    # 出现乱码时可以采用此行语句
    soup = BeautifulSoup(wb_data.text, 'lxml')
    return soup

def get_chnlUrl_from(url, headers):
    soup = get_soup(url, headers)
    chnl_urls = soup.select('div.main-pop dl dt a')
    for chnl_url in chnl_urls:
        data = {
            'url_st'  : False,       # status: True: done; False: not yet;
            'type'    : chnl_url.text,
            'chnl_url': host_url + chnl_url.get('href'),
        }
        w2_chnlUrl_col.insert_one(data)
    for type in ['手机号码', '消费卡券', '电影演出', '宠物狗', '奇趣小宠']:
        w2_chnlUrl_col.remove({'type': type})
    print('Done getting index urls.')
# get_chnlUrl_from(index_url, headers)

def get_itmUrl_from(url, headers, type, who_sells):
    soup = get_soup(url, headers)
    infos = soup.select('dd.feature > div > ul > li > a')
    for info in infos:
        data = {
            'itm_st'   : False,
            'url'      : info.get('href'),
            'type'     : type,
            'who_sells': who_sells,
        }
        w2_itmUrl_col.insert_one(data)
    time.sleep(1)

def get_itmUrls():
    col = w2_chnlUrl_col.find({'url_st':False})
    for doc in col:
        for who_sells in [1, 2]:
            page_num = 0
            while True:
                page_num += 1
                url = doc['chnl_url'] + 'a{}o{}'.format(who_sells, page_num)
                get_itmUrl_from(url, headers, doc['type'], who_sells)
                soup = get_soup(url, headers)
                if not soup.select('a.c.linkOn'):
                    break
        doc.update({'url_st': True})
        w2_chnlUrl_col.update({'_id': doc['_id']}, doc)
        print('Done getting item urls for %s' % doc['type'])

# get_itmUrls()

# 'a{}o{}'.format(who_sells, page_num) a1:personal a2:store
# if soup.select('a.c.linkOn') return [], then break the loop





