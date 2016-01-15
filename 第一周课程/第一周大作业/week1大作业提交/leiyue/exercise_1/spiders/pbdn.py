# -*- coding: utf-8 -*-

from __future__ import print_function

import re
from datetime import datetime

import requests
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule

from exercise_1.items import Exercise1Item
from exercise_1.misc import *


def serialize_id(text):
    return int(text) if text else None


def serialize_text(text):
    return text[0].strip() if text else None


def serialize_view(result):
    return int(result.split('=')[2]) if result else None


def serialize_date(date):
    return datetime.strptime(date[0].strip(), "%Y-%m-%d") if date else None


def serialize_price(number):
    return float(number[0].strip()) if number else None


def serialize_business(text):
    pattern = re.compile(r'（(.*)）')
    business = text[0].strip()
    return re.sub(pattern, r'\1', business) if business else u'个人'


def serialize_area(area):
    return ' - '.join(area) if area else None


def serialize_seller_id(url):
    return int(url[0].split('/')[3]) if url else None


def serialize_name(name):
    return name[0].strip() if name else None


class PbdnSpider(CrawlSpider):
    name = "pbdn"
    allowed_domains = ["bj.58.com"]
    start_urls = ('http://bj.58.com/pbdn/',)

    rules = (
        Rule(LinkExtractor(allow=r'/pbdn/', restrict_xpaths='//*[@id="infolist"]/div[5]/a'), follow=True),
        Rule(LinkExtractor(allow=r'/pingbandiannao/\d+x\.shtml', ), callback='parse_item', ),
    )

    # def parse(self, response):
    #     pass

    def parse_item(self, response):
        info('Parse Item: ' + response.url)
        pattern = re.compile(r'.*pingbandiannao/(\d+)x..*')
        sel = Selector(response)
        product_id = re.sub(pattern, r'\1', response.url)
        title = sel.xpath('//*[@id="content"]/div[1]/div[1]/div[1]/h1/text()').extract()
        view = requests.get('http://jst1.58.com/counter?infoid={id}'.format(id=product_id)).text
        date = sel.xpath('//*[@id="index_show"]/ul[1]/li[1]/text()').extract()
        price = sel.xpath('//span[@class="price c_f50"]/text()').extract()
        business = sel.xpath('//*[@id="tan_tishi"]/div/div[1]/div/p/span/text()').extract()
        area = sel.xpath('//ul/li/div[@class="su_con"]/span[@class="c_25d"]/a/text()').extract()
        category = sel.xpath('//*[@id="header"]/div[2]/span[3]/a/text()').extract()
        seller_id = sel.xpath('//p[@class="content_info"]/a/@href').extract()
        seller_name = sel.xpath('//*[@id="perAdRight"]/div[2]/ul/li[1]/a/text()').extract()
        seller_qq_name = sel.xpath('//div[@class="cont_imgPa"]/p/text()').extract()
        seller_alias = sel.xpath('//*[@id="tan_tishi"]/div/div[1]/div/p/text()').extract()

        item = Exercise1Item()
        item['id'] = serialize_id(product_id)
        item['title'] = serialize_text(title)
        item['view'] = serialize_view(view)
        item['date'] = serialize_date(date)
        item['price'] = serialize_price(price)
        item['business'] = serialize_business(business)
        item['area'] = serialize_area(area)
        item['category'] = serialize_text(category)
        item['seller_id'] = serialize_seller_id(seller_id)

        # item['seller_name'] = serialize_text(seller_name)
        # item['seller_qq_name'] = serialize_text(seller_qq_name)
        # item['seller_alias'] = serialize_text(seller_alias)

        yield item
