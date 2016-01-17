# -*- coding: utf-8 -*-

from __future__ import print_function

import re
from scrapy.selector import Selector
from scrapy.spiders import Spider
from shoujihao.misc import info
from shoujihao.items import ShoujihaoItem


def serialize_id(title):
    if not title:
        return None
    else:
        pattern = re.compile(r'.*(\d{11}).*')
        phone_number = re.sub(pattern, r'\1', title.strip())
        return int(phone_number) if phone_number else None


def serialize_price(number):
    if not number:
        return None
    else:
        pattern = re.compile(r'^(\d+).*')
        price = re.sub(pattern, r'\1', number.strip())
        return int(price) if price else None


def serialize_carrier(number):
    if not number:
        return None
    else:
        china_mobile = re.compile(r'^1(34[0-8]|705|(3[5-9]|47|5[0127-9]|78|8[23478])\d)\d{7}$')
        china_unicom = re.compile(r'^1((3[0-2]|45|5[56]|76|8[56])\d{8}|70[789]\d{7})$')
        china_telecom = re.compile(r'^1((33|53|7[67]|8[019])[0-9]|349|70[059])\d{7}$')
        if re.search(china_mobile, number):
            return unicode('中国移动', 'utf8')
        elif re.search(china_unicom, number):
            return unicode('中国联通', 'utf8')
        elif re.search(china_telecom, number):
            return unicode('中国电信', 'utf8')
        else:
            return None


class SjhmSpider(Spider):
    name = "sjhm"
    allowed_domains = ["bj.58.com"]
    start_urls = ["http://bj.58.com/shoujihao/pn%02d/" % num for num in range(1, 71)]

    def parse(self, response):
        info('Parse Items in Page: ' + response.url)

        sel = Selector(response)

        titles = sel.xpath('//*[@id="infolist"]/div/ul/div[@class="boxlist"]/ul/li/a[1]/strong/text()').extract()
        links = sel.xpath('//*[@id="infolist"]/div/ul/div[@class="boxlist"]/ul/li/a[1]/@href').extract()
        prices = sel.xpath('//*[@id="infolist"]/div/ul/div[@class="boxlist"]/ul/li/a[1]/b/text()').extract()

        for title, link, price in zip(titles, links, prices):
            item = ShoujihaoItem()
            item['id'] = serialize_id(title)
            item['link'] = link
            item['price'] = serialize_price(price)
            item['carrier'] = serialize_carrier(str(item['id']))

            # from pprint import pprint
            # pprint(item)

            yield item
