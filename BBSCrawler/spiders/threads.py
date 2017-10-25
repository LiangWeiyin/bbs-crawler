#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/24
# @Author  : ouyangsong
# @Contact : songouyang@live.com
# @File    : threads.py


import scrapy
from BBSCrawler.items import ThreadsItem
import json
from pymongo import MongoClient


class ThreadsSpider(scrapy.Spider):
    name = "threads"
    allowed_domains = ["bbs.byr.cn"]
    start_urls = "https://bbs.byr.cn/open/threads/{board}/{article_id}.json?&oauth_token={oauth_token}&page={page_num}"

    def start_requests(self):
        client = MongoClient(self.settings["MONGO_HOST"], self.settings["MONGO_PORT"])
        db = client[self.settings["MONGO_DATABASE"]]
        db.authenticate(self.settings["MONGO_USER"], self.settings["MONGO_PASSWORD"])
        articles = db["articles"]
        for item in articles.find({}, {"board_name": 1, "id": 1}):
            article_id = item["id"]
            board_name = item["board_name"]
            threads_url = self.start_urls.format(board=board_name, article_id=article_id,
                                                 oauth_token=self.settings["OAUTH_TOKEN"], page_num=1)
            yield scrapy.Request(threads_url, meta={"board_name": board_name, "article_id": article_id, "page_num": 1})

    def parse(self, response):
        dict_response = json.loads(response.body)
        item = ThreadsItem()
        if dict_response["article"]:
            for thread in dict_response["article"]:
                item["id"] = thread["id"]
                item["group_id"] = thread["group_id"]
                item["reply_id"] = thread["reply_id"]
                item["flag"] = thread["flag"]
                item["position"] = thread["position"]
                item["is_top"] = thread["is_top"]
                item["is_subject"] = thread["is_subject"]
                item["has_attachment"] = thread["has_attachment"]
                item["is_admin"] = thread["is_admin"]
                item["title"] = thread["title"]
                item["user"] = thread["user"]
                item["post_time"] = thread["post_time"]
                item["board_name"] = thread["board_name"]
                item["board_description"] = thread["board_description"]
                item["content"] = thread["content"]
                item["attachment"] = thread["attachment"]
                item["like_sum"] = thread["like_sum"]
                yield item

        if dict_response["pagination"]["page_current_count"] < dict_response["pagination"]["page_all_count"]:
            board_name = response.meta["board_name"]
            article_id = response.meta["article_id"]
            page_num = dict_response["pagination"]["page_current_count"] + 1
            threads_url = self.start_urls.format(board=board_name, article_id=article_id,
                                                 oauth_token=self.settings["OAUTH_TOKEN"], page_num=page_num)
            yield scrapy.Request(threads_url, meta={"board_name": board_name,
                                                    "article_id": article_id,
                                                    "page_num": page_num})
