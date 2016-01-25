# -*- coding: utf-8 -*-

from scrapy import Item, Field


class ShoujihaoItem(Item):
    id = Field()
    link = Field()
    price = Field()
    carrier = Field()
