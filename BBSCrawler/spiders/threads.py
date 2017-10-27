#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/24
# @Author  : ouyangsong
# @Contact : songouyang@live.com
# @File    : threads.py


import scrapy
from BBSCrawler.items import ThreadsItem
import json
from scrapy_redis.spiders import RedisCrawlSpider


class ThreadsSpider(RedisCrawlSpider):
    name = "threads"
    custom_settings = {
        'DOWNLOAD_DELAY': 4,
    }
    allowed_domains = ["bbs.byr.cn"]
    redis_key = 'threads:start_urls'

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
                self.logger.info("item:{}".format(thread["id"]))
                yield item

        if dict_response["pagination"]["page_current_count"] < dict_response["pagination"]["page_all_count"]:
            board_name = dict_response["board_name"]
            article_id = dict_response["id"]
            page_num = dict_response["pagination"]["page_current_count"] + 1
            yield scrapy.Request("https://bbs.byr.cn/open/threads/{board}/{article_id}.json?"
                                 "&oauth_token={oauth_token}&page={page_num}"
                                 "".format(board=board_name,
                                           article_id=article_id,
                                           oauth_token=self.settings["OAUTH_TOKEN"],
                                           page_num=page_num))
