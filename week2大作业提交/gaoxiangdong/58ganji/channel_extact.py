from bs4 import BeautifulSoup
import requests

headers = {
     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4',
     'Cookie': 'citydomain=bj; ganji_xuuid=1879886f-c902-44ec-89eb-ab28e0b0478a.1452608110409; ganji_uuid=5212120881512590752584; GANJISESSID=56073313f2a81dab106991dfbdffa334; hotPriceTip=1; STA_DS=0; lg=1; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A80111296479%7D; __utma=32156897.1500200464.1452608104.1452608104.1452696203.2; __utmb=32156897.17.10.1452696203; __utmc=32156897; __utmz=32156897.1452608104.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'

}
url = 'http://bj.ganji.com/wu/'
local_url = 'http://bj.ganji.com'

wb_data = requests.get(url)
soup = BeautifulSoup(wb_data.text , 'lxml')
links = soup.select('dl.fenlei > dt > a ')
for link in links :
    link = local_url + link.get('href')

channel_list = '''
http://bj.ganji.com/ruanjiantushu/
http://bj.ganji.com/yingyouyunfu/
http://bj.ganji.com/diannao/
http://bj.ganji.com/xianzhilipin/
http://bj.ganji.com/fushixiaobaxuemao/
http://bj.ganji.com/meironghuazhuang/
http://bj.ganji.com/shuma/
http://bj.ganji.com/laonianyongpin/
http://bj.ganji.com/xuniwupin/
http://bj.ganji.com/qitawupin/
http://bj.ganji.com/ershoufree/
http://bj.ganji.com/wupinjiaohuan/
'''
# channel_list = '''
# http://bj.ganji.com/jiaju/
# http://bj.ganji.com/rirongbaihuo/
# http://bj.ganji.com/shouji/
# http://bj.ganji.com/bangong/
# http://bj.ganji.com/nongyongpin/
# http://bj.ganji.com/jiadian/
# http://bj.ganji.com/ershoubijibendiannao/
# http://bj.ganji.com/ruanjiantushu/
# http://bj.ganji.com/yingyouyunfu/
# http://bj.ganji.com/diannao/
# http://bj.ganji.com/xianzhilipin/
# http://bj.ganji.com/fushixiaobaxuemao/
# http://bj.ganji.com/meironghuazhuang/
# http://bj.ganji.com/shuma/
# http://bj.ganji.com/laonianyongpin/
# http://bj.ganji.com/xuniwupin/
# http://bj.ganji.com/qitawupin/
# http://bj.ganji.com/ershoufree/
# http://bj.ganji.com/wupinjiaohuan/
# '''