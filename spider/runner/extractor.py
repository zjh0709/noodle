import json

from redis.client import Redis
from pymongo.database import Database

from spider.runner.config import ARTICLE_TABLE, KEYWORD_KEY
from spider.runner import utils

import logging

from functools import partial
from baidu.nlp import Nlp


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


def run_keyword(r: Redis, db: Database):
    save_article = partial(utils.save_document, db, ARTICLE_TABLE)
    nlp = Nlp()
    while r.exists(KEYWORD_KEY):
        article = json.loads(r.lpop(KEYWORD_KEY).decode())
        title = article.get("title", "")
        content = article.get("content", "")
        keywords = nlp.keyword(title, content)
        if article.get("url"):
            save_article({"url": article.get("url"), "keyword": keywords})
            logging.info("update keyword success. keyword: {}".format(keywords))
    logging.info("job complete.")
