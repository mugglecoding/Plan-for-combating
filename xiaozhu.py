from bs4 import BeautifulSoup
import requests,time

n = 30#一共抓起多少条数据
pages = int(n/24)+1 #每页24条数据,共pages页
urls = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i)) for i in range(pages)]


def get_host(url,data=[]):
    soup = BeautifulSoup(requests.get(url).text,"lxml")
    name = soup.select("div.fd_name")
    if name != [] :
        name = name[0].get_text().replace(" ","").replace('\n','')
        print(name)

def get_lodge(url,data=[]):
    count = 1
    soup = BeautifulSoup(requests.get(url).text,'lxml')
    titles = soup.select("span.result_title")
    imgs = soup.select("img.lodgeunitpic")
    addresses = soup.select("em.hiddenTxt")
    prices = soup.select("span.result_price > i")
    hosts = soup.select('a.="search_result_gridsum"')


    for title,img,address,price,host in zip(titles,imgs,addresses,prices,hosts):
        info = {
            "title":title.get_text().replace(" ",""),
            "img":img.get("lazy_src"),
            "address":address.get_text().replace(" ","").split("\n")[-1],
            "price":price.get_text().replace(" ",""),
            "host":host.get("href")
        }
        data.append(info)

    for i in data:
        if count<=n:
            #print('NO.'+str(count) + ', ' + i["title"] + ', ' + i["img"] + ', ' + i["address"] + ', ' + i["price"])
            print('NO.'+str(count),i["title"],i["img"],i["address"],i["price"])
            get_host(i["host"])
            count += 1
        else:
            print("The End")
            break

    time.sleep(3)

for url in urls:
    get_lodge(url)

