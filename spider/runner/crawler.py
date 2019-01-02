import json

from redis.client import Redis
from pymongo.database import Database

from spider.runner.config import STOCK_KEY, TOPIC_KEY, ARTICLE_TABLE
from spider.runner import utils
from spider.website.sina import SinaReport
from spider.website.jrj import JrjReport, JrjNews
from spider.website.eastmoney import EastmoneyReport

import logging

from spider.runner.config import stock

from functools import partial
from spider.entity import article_to_dict, dict_to_article


def _reset_key(r: Redis, k: str):
    logging.info("start reset `{}`...".format(k))
    if r.exists(k) > 0:
        logging.warning("key `{}` is exists. will delete it.".format(k))
        r.delete(k)
        logging.info("delete key `{}` success.".format(k))


def reset_topic(r: Redis):
    _reset_key(r, STOCK_KEY)
    r.rpush(STOCK_KEY, *stock)
    logging.info("reset `{}` success.".format(STOCK_KEY))


def reset_article(r: Redis, db: Database, num: int=1000):
    _reset_key(r, TOPIC_KEY)
    load_article = partial(utils.load_article, db, ARTICLE_TABLE)
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


def run_topic(r: Redis, db: Database, mode: str = "hot"):
    assert mode in ["hot", "all"]
    job_list = [JrjReport(), JrjNews(), SinaReport(), EastmoneyReport()]
    save_article = partial(utils.save_article, db, ARTICLE_TABLE)
    while r.exists(STOCK_KEY):
        code = r.lpop(STOCK_KEY).decode()
        logging.info("start stock {}...".format(code))
        for job in job_list:
            if mode == "hot":
                page = job.first_page(code)
                topics = job.get_topics_by_page(page)
            else:
                topics = job.get_topics_by_code(code)
            logging.info("stock {} job {} topics {}".format(code, job.__class__.__name__, len(topics)))
            for article in topics:
                # noinspection PyProtectedMember
                save_article(article._asdict())
        logging.info("stock {} success.".format(code))
    logging.info("job complete.")


def run_article(r: Redis, db: Database):
    job_map = {
        "jrj_report": JrjReport(),
        "jrj_news": JrjNews(),
        "sina_report": SinaReport(),
        "eastmoney_report": EastmoneyReport()
    }
    column_map = {
        "jrj_report": ["content", "author", "date"],
        "jrj_news": ["content", "org", "date"],
        "sina_report": ["title", "content", "author", "org", "date"],
        "eastmoney_report": ["content"]
    }
    save_article = partial(utils.save_article, db, ARTICLE_TABLE)
    while r.exists(TOPIC_KEY):
        article = json.loads(r.lpop(TOPIC_KEY).decode())
        url = article.get("url")
        logging.info("start article {}...".format(url))
        article = dict_to_article(article)
        job_type = article.domain + "_" + article.category
        job = job_map.get(job_type)
        if job:
            article = job.get_article_detail(article)
            column = column_map[job_type]
            article = article_to_dict(article)
            save_article(article, column)
            logging.info("save article success. url: {}".format(url))
    logging.info("job complete.")
