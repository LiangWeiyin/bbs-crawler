#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/25
# @Author  : ouyangsong
# @Contact : songouyang@live.com
# @File    : PushSectionName.py


from redis import Redis
from pymongo import MongoClient


def get_from_mongo(mongo_host, mongo_port, mongo_database, mongo_user, mongo_password):
    client = MongoClient(mongo_host, mongo_port)
    db = client[mongo_database]
    db.authenticate(mongo_user, mongo_password)
    for item in db["section"].find({}, {"board.name": 1}):
        for boards in item["board"]:
            yield boards["name"]


if __name__ == "__main__":
    host = "your_ip"
    port = 27017
    database = "BBS"
    user = "username"
    password = "password"

    start_url = "articles:start_urls"
    base_url = "https://bbs.byr.cn/open/board/{board}.json?&oauth_token=your_oauth_token&page=1"

    redis_port = 6379
    r = Redis(host=host, port=redis_port)
    r.flushall()
    for board in get_from_mongo(host, port, database, user, password):
        r.lpush(start_url, base_url.format(board=board))
