# -*- coding: utf-8 -*-

from scrapy import Item, Field


class Exercise1Item(Item):
    id = Field()
    title = Field()
    view = Field()
    date = Field()
    price = Field()
    business = Field()
    area = Field()
    category = Field()
    seller_id = Field()
    # seller_name = Field()
    # seller_qq_name = Field()
    # seller_alias = Field()
