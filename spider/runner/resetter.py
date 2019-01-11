import json

from redis.client import Redis
from pymongo.database import Database

from spider.runner.config import STOCK_KEY, TOPIC_KEY, STOCK_COMPLETE_KEY, KEYWORD_KEY
from spider.runner.config import ARTICLE_TABLE
from spider.runner import utils

import logging

from spider.runner.config import stock

from functools import partial


def reset_stock(r: Redis):
    utils.reset_key(r, STOCK_KEY)
    utils.reset_key(r, STOCK_COMPLETE_KEY)
    r.rpush(STOCK_KEY, *stock)
    logging.info("reset `{}` success.".format(STOCK_KEY))


def reset_topic(r: Redis, db: Database, num: int=1000):
    utils.reset_key(r, TOPIC_KEY)
    load_article = partial(utils.load_document, db, ARTICLE_TABLE)
    cursor = load_article(spec={"content": ""},
                          column=["url", "domain", "category"],
                          order={"uptime": 1},
                          limit=num)
    while True:
        try:
            article = cursor.next()
            r.rpush(TOPIC_KEY, json.dumps(article))
        except StopIteration:
            break
    cursor.close()
    logging.info("reset `{}` success.".format(TOPIC_KEY))


def reset_keyword(r: Redis, db: Database, num: int=1000):
    utils.reset_key(r, KEYWORD_KEY)
    load_article = partial(utils.load_document, db, ARTICLE_TABLE)
    cursor = load_article(spec={"content": {"$ne": ""}, "keyword": {"$exists": False}},
                          column=["url", "title", "content"],
                          order={"uptime": 1},
                          limit=num)
    while True:
        try:
            article = cursor.next()
            r.rpush(KEYWORD_KEY, json.dumps(article))
        except StopIteration:
            break
    cursor.close()
    logging.info("reset `{}` success.".format(KEYWORD_KEY))
