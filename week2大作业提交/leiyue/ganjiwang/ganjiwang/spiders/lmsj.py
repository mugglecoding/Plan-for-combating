# -*- coding: utf-8 -*-

from __future__ import print_function

import re
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ganjiwang.misc import info
from ganjiwang.items import GanjiwangItem


class LmsjSpider(CrawlSpider):
    name = "lmsj"
    allowed_domains = ["bj.ganji.com"]
    categories = [
        'jiaju', 'rirongbaihuo', 'shouji', 'shoujihaoma', 'bangong', 'nongyongpin',
        'jiadian', 'ershoubijibendiannao', 'ruanjiantushu', 'yingyouyunfu', 'diannao',
        'xianzhilipin', 'fushixiaobaxuemao', 'meironghuazhuang', 'shuma', 'laonianyongpin',
        'xuniwupin', 'qitawupin', 'ershoufree', 'wupinjiaohuan',
    ]
    # categories = ['jiaju']
    allow_rules = [r'/%s/' % category for category in categories]

    @staticmethod
    def generator(self, categories):
        for category in categories:
            yield 'http://bj.ganji.com/%s/' % category
            yield 'http://bj.ganji.com/%s/a2/' % category

    start_urls = list(generator(categories))

    rules = [
        Rule(LinkExtractor(
                allow=allow_rules,
                restrict_xpaths='//*[@id="wrapper"]/div[5]/div[7]/ul/li/a'
        ), follow=True),
        Rule(LinkExtractor(
                allow=allow_rules,
                restrict_xpaths='//*[@id="wrapper"]/div[5]/div[4]/dl/dd[1]/div/ul/li/a'
        ), callback='parse_item'),

    ]

    @staticmethod
    def parse_item(response):
        info('Parse Items: ' + response.url)
        id_pattern = re.compile(r'.*([0-9]{10})')
        date_pattern = re.compile(r'([0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}).*')
        sel = Selector(response)

        item = GanjiwangItem()
        item['id'] = re.sub(
                id_pattern,
                r'\1',
                sel.xpath('//*[@id="wrapper"]/div[3]/div[1]/div[4]/div[1]/div/text()').extract()[0])
        item['title'] = sel.xpath('//*[@id="wrapper"]/div[3]/div[1]/div[1]/h1/text()').extract()[0].split(' - ')[0]
        item['date'] = re.sub(
                date_pattern,
                r'\1',
                sel.xpath('//*[@id="wrapper"]/div[3]/div[1]/div[1]/div/ul[2]/li[1]/i/text()').extract()[0].strip())
        item['category'] = sel.xpath('//*[@id="wrapper"]/div[3]/div[1]/div[3]/div/ul/li[1]/span/a/text()').extract()[0]
        item['price'] = sel.xpath('//*[@id="wrapper"]/div[3]/div[1]/div[3]/div/ul/li[2]/i[1]/text()').extract()[0]
        item['address'] = '-'.join(
                sel.xpath('//*[@id="wrapper"]/div[3]/div[1]/div[3]/div/ul/li[3]/a/text()').extract()
        ).strip()

        # for key in item.keys():
        #     print(item[key])

        yield item
