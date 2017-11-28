#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/26
# @Author  : ouyangsong
# @Contact : songouyang@live.com
# @File    : PushArticlesId.py


from redis import Redis
from pymongo import MongoClient


def get_from_mongo(mongo_host, mongo_port, mongo_database, mongo_user, mongo_password):
    client = MongoClient(mongo_host, mongo_port)
    db = client[mongo_database]
    db.authenticate(mongo_user, mongo_password)
    for item in db["articles"].find({}, {"id": 1, "board_name": 1}, no_cursor_timeout = True):
        yield {"board_name": item["board_name"], "id": item["id"]}


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 27017
    database = "BBS"
    user = "username"
    password = "password"

    start_url = "threads:start_urls"
    base_url = "https://bbs.byr.cn/open/threads/{board_name}/{id}.json?" \
               "&oauth_token=your_oauth_token&page=1"

    redis_port = 6379
    r = Redis(host=host, port=redis_port)
    r.flushall()

    for article_info in get_from_mongo(host, port, database, user, password):
        r.lpush(start_url, base_url.format(board_name=article_info["board_name"], id=article_info["id"]))
