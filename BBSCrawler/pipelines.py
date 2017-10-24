# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import pymongo


class BbscrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.section_names_seen = set()

    def process_item(self, item, spider):
        if spider.name == "section":
            if item["name"] in self.section_names_seen:
                raise DropItem("Duplicate section {} found".format(item["name"]))
            else:
                self.section_names_seen.add(item["name"])
                return item

        if spider.name in ["articles", "threads"]:
            if item["id"] in self.section_names_seen:
                raise DropItem("Duplicate article, id:{}".format(item["id"]))
            else:
                self.section_names_seen.add(item["id"])
                return item

        else:
            return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DATABASE', 'BBS')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == "section":
            self.db["section"].insert(dict(item))
            return item
        elif spider.name == "articles":
            self.db["articles"].insert(dict(item))
            return item
        elif spider.name == "threads":
            self.db["threads"].insert(dict(item))
            return item
        else:
            return item
