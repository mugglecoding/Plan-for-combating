# -*- coding: utf-8 -*-

from __future__ import print_function

from scrapy.exceptions import DropItem


class DuplicatesPipeline(object):
    def __init__(self):
        self.ids = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids:
            raise DropItem("Duplicate item found: %s" % item['id'])
        else:
            self.ids.add(item['id'])
            return item