from bs4 import BeautifulSoup
import requests


wb_data = requests.get('http://bj.ganji.com/wu/','utf-8')
wb_data.encoding = 'utf-8'
soup = BeautifulSoup(wb_data.text,'lxml')

#print (soup.prettify())

mum_url = 'http://bj.ganji.com'
titles = soup.select('dl.fenlei > dt > a')
urls = soup.select('dl.fenlei > dt > a')
category = []
caturl = []

for title,url in zip(titles,urls):
    category.append(title.get_text())
    caturl.append(mum_url+url.get('href'))

print (caturl)
print (category)


