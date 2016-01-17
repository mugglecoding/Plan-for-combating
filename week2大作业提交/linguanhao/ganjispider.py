import requests
import time
import pymongo
from bs4 import BeautifulSoup
from pybloom import BloomFilter
import os
import re
import random
import socket

from threading import Thread,Lock
from multiprocessing import Pool

client = pymongo.MongoClient('localhost', 27017)

channel_db = client['channel_urls']
channel_urls_sheet = channel_db['url_lists']

items_db = client['item_urls']
# item_urls_sheet = items_db['url_lists']
# item_urls_repeat_sheet = items_db['url_lists_repeat']
item_urls_sheet = items_db['url_lists']
item_urls_repeat_sheet = items_db['url_lists_repeat_append']

info_db = client['item_infos']
info_sheet = info_db['info_table']

log_file_name = 'error.log'
log_file_path = os.path.join(os.path.dirname(__file__), log_file_name)


class ChannelSpider:
    '''爬取所有频道的url连接'''
    def __init__(self, url):
        self.url = url

    def get_channel_urls(self):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/47.0.2526.106 Safari/537.36'
        }
        response = requests.get(self.url, headers=header)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        channels = soup.select('dl.fenlei dt a')
        channels_url = ['http://bj.ganji.com' +
                        each.get('href') for each in channels]
        return channels_url

    def run(self):
        if channel_urls_sheet: # 重新创建数据库
            channel_urls_sheet.drop()
        channels_urls = self.get_channel_urls()
        for channel_url in channels_urls:
            channel_urls_sheet.insert_one({'url': channel_url})


class ItemSpider:
    def __init__(self, start=1):
        self.bloomfilter = BloomFilter(
                capacity=1000000, error_rate=0.001)
        # if item_urls_sheet:
        #     item_urls_sheet.drop()
        # if item_urls_repeat_sheet:
        #     item_urls_repeat_sheet.drop()


    def run(self):
        channel_urls = self.read_channel_urls_from_database()
        pool = Pool(processes=4)
        pool.map(self.multi_thread, channel_urls)


    def multi_thread(self, channel_url):
        whosells = ['a2','']
        for whosell in whosells:
            repeat_time = 1
            empty_page_check = 1
            page_num = 1
            while True:
                try:
                    self.get_items_from_urls(channel_url, page_num, whosell)
                    page_num += 1
                    sleep_time = random.uniform(1,5)
                    time.sleep(sleep_time)
                except ReapeatPageError as e:
                    print(str(e) + '\t' + (str(channel_url + '{}'.format(whosell) + 'o{}'.format(page_num) + '\n')))
                    if repeat_time != 5: # 只有连续检测到五个重复页面时才判断该频道结束
                        page_num += 1
                        repeat_time += 1
                        continue
                    else:
                        break
                except EmptyPageError as e:
                    print(str(e) + '\t' + (str(channel_url + '{}'.format(whosell) + 'o{}'.format(page_num) + '\n')))
                    if empty_page_check != 5: # 如果被识别为爬虫，要求输入验证码或者真的遇到了空页，那就重复五次检测该页面
                        time.sleep(10)
                        empty_page_check += 1
                        continue
                    else:
                        break
                except: # 可能遇到服务器拒绝连接等其他异常，休眠五秒钟后再继续抓取该页面
                    print('others exception')
                    time.sleep(5)
                    continue

    def read_channel_urls_from_database(self):
        channle_urls = []
        for item in channel_urls_sheet.find():
            channle_urls.append(item['url'])
        return channle_urls

    def get_items_from_urls(self, channel_url, page_num, whosell=''):
        url = str(channel_url) + '{}'.format(whosell) + 'o{}'.format(page_num)
        # print(url)
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/47.0.2526.106 Safari/537.36',
            'Cookie': 'citydomain=bj; ganji_xuuid=dfd368f8-4e08-4b74-dd93-54417682d842.1452685440333; ganji_uuid=7942709232803383366592; GANJISESSID=5f1b917890c315c1e851075cccc121b8; hotPriceTip=1; SiftRecord[\'1452771318\']=%E5%9C%86%E6%A1%8C%E9%85%92%E5%BA%97%E5%AE%B4%E4%BC%9A%E6%A1%8C%E6%A4%85%E9%A3%9F%E5%A0%82...%7C%7C%2Fwu%2Fs%2F_%25E5%259C%2586%25E6%25A1%258C%25E9%2585%2592%25E5%25BA%2597%25E5%25AE%25B4%25E4%25BC%259A%25E6%25A1%258C%25E6%25A4%2585%25E9%25A3%259F%25E5%25A0%2582%25E6%25A1%258C%25E6%25A4%2585%2F; vip_version=new; cityDomain=bj; mobversionbeta=3g; wap_list_view_type=text; __utmganji_v20110909=0xa2c0c5e0c02f680cbd3c9c890af6c8c; statistics_clientid=me; codecheck=1; GanjiUserName=test159; GanjiUserInfo=%7B%22user_id%22%3A607132908%2C%22email%22%3A%22%22%2C%22username%22%3A%22test159%22%2C%22user_name%22%3A%22test159%22%2C%22nickname%22%3A%22%22%7D; bizs=%5B%5D; supercookie=AwN3ZGZlBGN4WQDkAQx1Z2R0LmMzZwD3ZwV5ZTIzLmDkZTWzBTL4LzSwMTEzAJVlZmD%3D; sscode=%2FVn6oNLABpQjaD5J%2FV8zbUjN; LastLoginTime=116-1-15; __utmt=1; STA_DS=1; lg=1; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A71040413794%2C%22kw%22%3A%22%E5%9C%86%E6%A1%8C%E9%85%92%E5%BA%97%E5%AE%B4%E4%BC%9A%E6%A1%8C%E6%A4%85%E9%A3%9F%E5%A0%82%E6%A1%8C%E6%A4%85%22%7D; __utma=32156897.172575094.1452685440.1452771123.1452821297.9; __utmb=32156897.25.10.1452821297; __utmc=32156897; __utmz=32156897.1452735144.4.4.utmcsr=bj.ganji.com|utmccn=(referral)|utmcmd=referral|utmcct=/wu/'
        }

        ip_addr = {
            '218.95.54.23',
            '49.84.105.216',
            '115.223.227.243',
            '113.218.84.212',
            '1.63.252.70',
            '119.7.93.219',
            '115.223.255.131',
            '112.195.85.93',
            '183.130.95.28',
            '182.105.10.203',
            '115.223.254.7',
            '220.187.209.222',
            '115.151.202.39',
            '115.218.120.30',
            '59.32.21.158',
            '120.195.198.49',
            '120.195.193.43',
            '125.40.224.24',
            '1.60.157.5',
            '59.62.36.71',
            '171.38.42.114',
            '115.223.249.204',
            '120.195.196.167',
            '221.227.38.59',
            '120.52.73.26',
            '115.150.14.52',
            '221.131.114.45',
            '116.27.105.56',
            '117.25.72.99'
        }

        # 动态ip？
        real_create_conn = socket.create_connection
        def set_src_addr(*args):
            address, timeout = args[0], args[1]
            ip = random.choice(ip_addr)
            source_address = (ip, 0)
            return real_create_conn(address, timeout, source_address)
        socket.create_connection = set_src_addr

        response = requests.get(url, headers=header)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')

        special = ['http://bj.ganji.com/qitawupin/',  # 这三个频道的爬取方式有异于其他频道
                   'http://bj.ganji.com/ershoufree/',
                   'http://bj.ganji.com/wupinjiaohuan/']
        if channel_url in special:
            raw_item_urls = soup.select('dt div.infor01 a.infor-title01.com-title')
        else:
            raw_item_urls = soup.select('div.layoutlist ul a.ft-tit')
        item_urls = []
        for each in raw_item_urls:
            temp = each.get('gjalog')
            if not temp:
                item_url = each.get('href')
            else:
                url_pattern = re.findall(
                        "@gjaddata=\D\d{0,10}:\D\d{0,10}:\D\d{0,10}:(.*?)}}",
                        temp, re.S)
                if not url_pattern:
                    item_num = re.findall('@puid=(.*?)@', temp, re.S)[0]
                else:
                    item_num = re.findall(
                            "@gjaddata=\D\d{0,10}:\D\d{0,10}:\D\d{0,10}:(.*?)}}",
                            temp, re.S)[0]
                item_url = 'http://bj.ganji.com/jiaju/' + item_num + 'x.htm'
            item_urls.append(item_url)
        # print(item_urls)
        print(url, len(item_urls))
        if not raw_item_urls:
            raise EmptyPageError('This is an empty page!')

        identify = 1 if not whosell else 2 # 个人卖家则identify=1
        if all(each in self.bloomfilter for each in item_urls): # 如果该页面内的url全部都被布隆过滤器命中，则认为该页面已经重复了
            raise ReapeatPageError('Page repeated!')
        for each in item_urls:
            if not each in self.bloomfilter:
                self.bloomfilter.add(each)
                item_urls_sheet.insert_one({'url': each, 'identify': identify, 'parenturl': url})
            else:
                item_urls_repeat_sheet.insert_one({'url': each, 'parenturl': url})
                continue

class InfoSpider:
    def __init__(self):
        self.lock = Lock()

    def run(self):
        for i in range(0,5):
            thread = Thread(target=self.multi_thread, args=('Thread-{}'.format(i),))
            thread.start()

    def multi_thread(self, name):
        num_of_url = item_urls_sheet.count()
        # print(num_of_url)
        index = 0
        while index <= num_of_url: # 循环提取数据库里的记录
            empty_page_check = 0
            num_of_url = item_urls_sheet.count()
            print(name +'--->'+ '   index: ' + str(index) + '\tnum_of_url: ' + str(num_of_url))
            if empty_page_check == 0:
                with self.lock:
                    collection = item_urls_sheet.find_one_and_delete({},{"url":1, "identify":1})
                url = collection['url']
                identify = collection['identify']
            else:
                print('正在重抓：',url)
            # print(url)
            try:
                # print(url)
                self.get_info(url, identify)
                if empty_page_check == 0:
                    index += 1
                sleep_time = random.uniform(0,5)
                time.sleep(sleep_time)
            except EmptyPageError as e:
                print(str(e) + '\t' + (str(url + '\n')))
                if empty_page_check != 5:
                    time.sleep(5)
                    empty_page_check += 1
                    continue
                else:
                    break
            except:
                print('others exception')
                time.sleep(5)
                continue

    def get_info(self, url, identify):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/47.0.2526.106 Safari/537.36',
            'Cookie':'citydomain=bj; ganji_xuuid=dfd368f8-4e08-4b74-dd93-54417682d842.1452685440333; ganji_uuid=7942709232803383366592; GANJISESSID=5f1b917890c315c1e851075cccc121b8; hotPriceTip=1; SiftRecord[\'1452771318\']=%E5%9C%86%E6%A1%8C%E9%85%92%E5%BA%97%E5%AE%B4%E4%BC%9A%E6%A1%8C%E6%A4%85%E9%A3%9F%E5%A0%82...%7C%7C%2Fwu%2Fs%2F_%25E5%259C%2586%25E6%25A1%258C%25E9%2585%2592%25E5%25BA%2597%25E5%25AE%25B4%25E4%25BC%259A%25E6%25A1%258C%25E6%25A4%2585%25E9%25A3%259F%25E5%25A0%2582%25E6%25A1%258C%25E6%25A4%2585%2F; vip_version=new; cityDomain=bj; mobversionbeta=3g; wap_list_view_type=text; __utmganji_v20110909=0xa2c0c5e0c02f680cbd3c9c890af6c8c; statistics_clientid=me; codecheck=1; GanjiUserName=test159; GanjiUserInfo=%7B%22user_id%22%3A607132908%2C%22email%22%3A%22%22%2C%22username%22%3A%22test159%22%2C%22user_name%22%3A%22test159%22%2C%22nickname%22%3A%22%22%7D; bizs=%5B%5D; supercookie=AwN3ZGZlBGN4WQDkAQx1Z2R0LmMzZwD3ZwV5ZTIzLmDkZTWzBTL4LzSwMTEzAJVlZmD%3D; sscode=%2FVn6oNLABpQjaD5J%2FV8zbUjN; LastLoginTime=116-1-15; __utmt=1; STA_DS=1; lg=1; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A71040413794%2C%22kw%22%3A%22%E5%9C%86%E6%A1%8C%E9%85%92%E5%BA%97%E5%AE%B4%E4%BC%9A%E6%A1%8C%E6%A4%85%E9%A3%9F%E5%A0%82%E6%A1%8C%E6%A4%85%22%7D; __utma=32156897.172575094.1452685440.1452771123.1452821297.9; __utmb=32156897.25.10.1452821297; __utmc=32156897; __utmz=32156897.1452735144.4.4.utmcsr=bj.ganji.com|utmccn=(referral)|utmcmd=referral|utmcct=/wu/'
        }

        ip_addr = {
            '218.95.54.23',
            '49.84.105.216',
            '115.223.227.243',
            '113.218.84.212',
            '1.63.252.70',
            '119.7.93.219',
            '115.223.255.131',
            '112.195.85.93',
            '183.130.95.28',
            '182.105.10.203',
            '115.223.254.7',
            '220.187.209.222',
            '115.151.202.39',
            '115.218.120.30',
            '59.32.21.158',
            '120.195.198.49',
            '120.195.193.43',
            '125.40.224.24',
            '1.60.157.5',
            '59.62.36.71',
            '171.38.42.114',
            '115.223.249.204',
            '120.195.196.167',
            '221.227.38.59',
            '120.52.73.26',
            '115.150.14.52',
            '221.131.114.45',
            '116.27.105.56',
            '117.25.72.99'
        }

        real_create_conn = socket.create_connection
        def set_src_addr(*args):
            address, timeout = args[0], args[1]
            ip = random.choice(ip_addr)
            source_address = (ip, 0)
            return real_create_conn(address, timeout, source_address)
        socket.create_connection = set_src_addr

        response = requests.get(url, headers=header)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')

        title = soup.select('div.col-cont.title-box h1')
        price = soup.select('div ul.det-infor li i.f22.fc-orange.f-type')
        type = soup.select('ul.det-infor li span a')
        area = soup.select('div.det-laybox ul.det-infor li')
        date = soup.select('div ul.title-info-l.clearfix li i.pr-5')

        if all( not each for each in [title, price, type, area, date]):
            raise EmptyPageError('验证码出现了或者是空页面')

        data = {
            'title': title[0].text.strip() if title else None,
            'price': price[0].text.strip() if price else None,
            'type': type[0].text if type else None,
            'area': ''.join(list(area[2].stripped_strings)[1:]) if area else None,
            'date': date[0].text.strip('\n').strip().replace('\xa0', '') if date else None,
            'identify': '个人' if identify == 1 else '商家'
        }

        info_sheet.insert_one({'info': data})

class EmptyPageError(ValueError):
    pass

class ReapeatPageError(ValueError):
    pass

class EndPageError(ValueError):
    pass


if __name__ == '__main__':
    channel_spider = ChannelSpider('http://bj.ganji.com/wu/')
    channel_spider.run()

    item_spider = ItemSpider()
    item_spider.run()

    info_spider = InfoSpider()
    info_spider.run()

