# -*- coding: utf-8 -*-

from __future__ import print_function

from datetime import datetime

from scrapy import Item, Field


def serialize_id(item_id):
    return int(item_id) if item_id else None


def serialize_text(text):
    return text.strip() if text else None


def serialize_date(date):
    if not date:
        return None
    else:
        now = datetime.now()
        published_at = datetime.strptime(date.strip(), "%m-%d %H:%M").replace(year=now.year)

        print(published_at, now)

        if published_at > now:
            try:
                return published_at.replace(year=published_at.year - 1)
            except ValueError:
                # Must be 2/29!
                assert published_at.month == 2 and published_at.day == 29  # can be removed
                return published_at.replace(month=2, day=28,
                                            year=published_at.year - 1)
        else:
            return published_at


def serialize_price(price):
    return int(price.strip()) if price else None


class GanjiwangItem(Item):
    id = Field(serializer=serialize_id)
    title = Field(serializer=serialize_text)
    date = Field(serializer=serialize_date)
    category = Field(serializer=serialize_text)
    price = Field(serializer=serialize_price)
    address = Field(serializer=serialize_text)
