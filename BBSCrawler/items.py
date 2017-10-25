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
    group_id = scrapy.Field()
    reply_id = scrapy.Field()
    flag = scrapy.Field()
    position = scrapy.Field()
    is_top = scrapy.Field()
    is_subject = scrapy.Field()
    has_attachment = scrapy.Field()
    is_admin = scrapy.Field()
    title = scrapy.Field()
    user = scrapy.Field()
    post_time = scrapy.Field()
    board_name = scrapy.Field()
    board_description = scrapy.Field()
    reply_count = scrapy.Field()
    last_reply_user_id = scrapy.Field()
    last_reply_time = scrapy.Field()


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
