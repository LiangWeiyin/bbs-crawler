# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BbscrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SectionItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    is_root = scrapy.Field()
    parent = scrapy.Field()
    sub_section = scrapy.Field()
    board = scrapy.Field()