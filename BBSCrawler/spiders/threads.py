#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/24
# @Author  : ouyangsong
# @Contact : songouyang@live.com
# @File    : threads.py


import scrapy
from BBSCrawler.items import ThreadsItem
import json
import pymongo


class ThreadsSpider(scrapy.Spider):
    name = "threads"
    allowed_domains = ["prod.niuap.com"]

    def start_requests(self):
        client = pymongo.MongoClient(self.settings["MONGO_URI"])
        sections = client[self.settings["MONGO_DATABASE"]]
        boards = sections["articles"]
        for item in boards.find({}, {"board": 1, "id": 1}):
            article_id = item["id"]
            board_id = item["board"]
            threads_url = "https://prod.niuap.com/cangjie/article/threads/{board_id}/{article_id}?" \
                          "page={page_num}".format(board_id=board_id, article_id=article_id, page_num=1)
            yield scrapy.Request(threads_url, meta={"board_id": board_id, "article_id": article_id, "page_num": 1})

    def parse(self, response):
        dict_response = json.loads(response.body)
        item = ThreadsItem()
        if dict_response["article"]:
            for thread in dict_response["article"]:
                item["id"] = thread["id"]
                item["group_id"] = thread["group_id"]
                item["reply_id"] = thread["reply_id"]
                item["is_subject"] = thread["is_subject"]
                item["title"] = thread["title"]
                item["user"] = thread["user"]
                item["post_time"] = thread["post_time"]
                item["board_name"] = thread["board_name"]
                item["board_name_en"] = thread["board_name_en"]
                item["content"] = thread["content"]
                yield item

        if dict_response["pagination"]["page_current_count"] < dict_response["pagination"]["page_all_count"]:
            board_id = response.meta["board_id"]
            article_id = response.meta["article_id"]
            page_num = int(dict_response["pagination"]["page_current_count"]) + 1
            threads_url = "https://prod.niuap.com/cangjie/article/threads/{board_id}/{article_id}?" \
                          "page={page_num}".format(board_id=board_id, article_id=article_id, page_num=page_num)
            yield scrapy.Request(threads_url, meta={"board_id": board_id, "article_id": article_id, "page_num": 1})
