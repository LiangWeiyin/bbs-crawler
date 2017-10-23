#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/23
# @Author  : ouyangsong
# @Contact : songouyang@live.com
# @File    : section.py


import scrapy
from BBSCrawler.items import SectionItem
import json


class SecitonSpider(scrapy.Spider):
    name = "section"
    allowed_domains = ["prod.niuap.com"]
    start_urls = ["https://prod.niuap.com/cangjie/board/section/{}.json".format(i) for i in range(10)]

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse, dont_filter=True)

    def parse(self, response):
        dict_response = json.loads(response.body)
        item = SectionItem()
        item["name"] = dict_response["name"]
        item["description"] = dict_response["description"]
        item["is_root"] = dict_response["is_root"]
        item["parent"] = dict_response["parent"]
        item["sub_section"] = dict_response["sub_section"]
        item["board"] = dict_response["board"]

        if dict_response["sub_section"]:
            subsection_urls = ["https://prod.niuap.com/cangjie/board/section/{}.json".format(sub_section)
                               for sub_section in item['sub_section']]
            for u in subsection_urls:
                yield scrapy.Request(u, callback=self.parse, dont_filter=True)
        self.logger.info("section: {} has been downloaded".format(item["name"]))
        yield item
