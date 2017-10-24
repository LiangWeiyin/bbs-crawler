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


class ArticlesItem(scrapy.Item):
    id = scrapy.Field()
    tid = scrapy.Field()
    theme = scrapy.Field()
    author_id = scrapy.Field()
    author_name = scrapy.Field()
    content = scrapy.Field()
    create_time = scrapy.Field()
    board = scrapy.Field()
    url = scrapy.Field()
    ip = scrapy.Field()
    ismain = scrapy.Field()
    mid = scrapy.Field()
    board_name_cn = scrapy.Field()

class ThreadsItem(scrapy.Item):
    id = scrapy.Field()
    group_id = scrapy.Field()
    reply_id = scrapy.Field()
    is_subject = scrapy.Field()
    title = scrapy.Field()
    user = scrapy.Field()
    post_time = scrapy.Field()
    board_name = scrapy.Field()
    board_name_en = scrapy.Field()
    content = scrapy.Field()
