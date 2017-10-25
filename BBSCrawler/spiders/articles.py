#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/23
# @Author  : ouyangsong
# @Contact : songouyang@live.com
# @File    : articles.py


import scrapy
from BBSCrawler.items import ArticlesItem
import json
from scrapy_redis.spiders import RedisCrawlSpider


class ArticlesSpider(RedisCrawlSpider):
    # 主要抓取各个板块的文章列表
    name = "articles"
    allowed_domains = ["bbs.byr.cn"]
    redis_key = 'articles:start_urls'

    def parse(self, response):
        dict_response = json.loads(response.body, encoding='utf-8')
        for article in dict_response["article"]:
            item = ArticlesItem()
            item["id"] = article["id"]
            item["group_id"] = article["group_id"]
            item["reply_id"] = article["reply_id"]
            item["flag"] = article["flag"]
            item["position"] = article["position"]
            item["is_top"] = article["is_top"]
            item["is_subject"] = article["is_subject"]
            item["has_attachment"] = article["has_attachment"]
            item["is_admin"] = article["is_admin"]
            item["title"] = article["title"]
            item["user"] = article["user"]
            item["post_time"] = article["post_time"]
            item["board_name"] = article["board_name"]
            item["board_description"] = article["board_description"]
            item["reply_count"] = article["reply_count"]
            item["last_reply_user_id"] = article["last_reply_user_id"]
            item["last_reply_time"] = article["last_reply_time"]
            self.logger.info(item["id"])
            yield item

        if dict_response["pagination"]["page_current_count"] < dict_response["pagination"]["page_all_count"]:
            board = dict_response["name"]
            page_num = dict_response["pagination"]["page_current_count"] + 1
            self.logger.info("board: {board}, pagenum: {page_num}".format(board=board, page_num=page_num))
            yield scrapy.Request("https://bbs.byr.cn/open/board/{board}.json?&oauth_token={oauth_token}"
                                 "&page={page_num}".format(board=board,
                                                           oauth_token=self.settings["OAUTH_TOKEN"], page_num=page_num),
                                 meta={'board': board, 'page_num': 1},
                                 callback=self.parse)
