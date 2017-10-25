# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from pymongo import MongoClient


class BbscrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.section_names_seen = set()
        self.article_names_seen = set()
        self.thread_names_seen = set()

    def process_item(self, item, spider):
        if spider.name == "section":
            if item["name"] in self.section_names_seen:
                raise DropItem("Duplicate section {} found".format(item["name"]))
            else:
                self.section_names_seen.add(item["name"])
                return item

        elif spider.name == "articles":
            if item["board_name"]+str(item["id"]) in self.article_names_seen:
                raise DropItem("Duplicate article, id:{id}, board:{board_name}".format(
                    id=item["id"], board_name=item["board_name"]))
            else:
                self.article_names_seen.add(item["board_name"]+str(item["id"]))
                return item

        elif spider.name == "threads":
            if item["board_name"]+str(item["id"]) in self.thread_names_seen:
                raise DropItem("Duplicate thread, id:{id}, board:{board_name}".format(
                    id=item["id"], board_name=item["board_name"]))
            else:
                self.thread_names_seen.add(item["board_name"]+str(item["id"]))
                return item

        else:
            return item


class MongoPipeline(object):
    def __init__(self, mongo_host, mongo_port, mongo_db, mongo_user, mongo_password):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db
        self.mongo_user = mongo_user
        self.mongo_password = mongo_password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGO_HOST'),
            mongo_port=crawler.settings.get('MONGO_POST'),
            mongo_db = crawler.settings.get('MONGO_DATABASE'),
            mongo_user=crawler.settings.get('MONGO_USER'),
            mongo_password=crawler.settings.get('MONGO_PASSWORD')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_host, int(self.mongo_port))
        self.db = self.client[self.mongo_db]
        self.db.authenticate(self.mongo_user, self.mongo_password)

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
