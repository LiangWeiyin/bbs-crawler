#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/23
# @Author  : ouyangsong
# @Contact : songouyang@live.com
# @File    : articles.py


import scrapy
from BBSCrawler.items import ArticlesItem
import json
import pymongo


class ArticlesSpider(scrapy.Spider):
    name = "articles"
    allowed_domains = ["prod.niuap.com"]

    def start_requests(self):
        client = pymongo.MongoClient(self.settings["MONGO_URI"])
        print(self.settings["MONGO_DATABASE"])
        sections = client[self.settings["MONGO_DATABASE"]]
        boards = sections["section"]
        for item in boards.find({}, {"board.name": 1}):
            for i in item["board"][1:2]:
                yield scrapy.Request("https://prod.niuap.com/cangjie/board/articles?boardName={}".format(i["name"]),
                                     meta={'board': i["name"]}, callback=self.parse)

    def parse(self, response):
        print(response.body)
        dict_response = json.loads(response.body, encoding='utf-8')
        item = ArticlesItem()

        for article in dict_response["data"]:
            item["id"] = article["id"]
            item["tid"] = article["tid"]
            item["theme"] = article["theme"]
            item["author_id"] = article["author_id"]
            item["author_name"] = article["author_name"]
            item["content"] = article["content"]
            item["create_time"] = article["create_time"]
            item["board"] = article["board"]
            item["url"] = article["url"]
            item["ip"] = article["ip"]
            item["ismain"] = article["ismain"]
            item["mid"] = article["mid"]
            item["board_name_cn"] = article["board_name_cn"]
            yield item

        if dict_response["data"]:
            last_id = dict_response["data"][-1]["id"]
            board = response.meta["board"]
            yield scrapy.Request("https://prod.niuap.com/cangjie/board/articles"
                                 "?boardName={board}&id={id}".format(board=board, id=last_id), meta={'board': board},
                                 callback=self.parse)
