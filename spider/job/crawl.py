import json

from redis.client import Redis
from pymongo.database import Database

from spider.website.sina import SinaReport
from spider.website.jrj import JrjReport, JrjNews
from spider.website.eastmoney import EastmoneyReport

import logging

from spider.job.config import stock
from spider.job import utils

from functools import partial
from spider.entity import Article


def reset_topic(r: Redis):
    logging.info("start reset `stock`...")
    if r.exists("stock") > 0:
        logging.warning("key `stock` is exists. will delete it.")
        r.delete("stock")
        logging.info("delete key `stock` success.")
    r.rpush("stock", *stock)
    logging.info("reset `stock` success.")


def reset_article(r: Redis, db: Database, num: int=1000):
    logging.info("start restart `article`...")
    if r.exists("article") > 0:
        logging.warning("key `article` is exists. will delete it.")
        r.delete("article")
        logging.info("delete key `article` success.")
    load_article = partial(utils.load_article, db)
    cursor = load_article(spec={"content": ""},
                          column=["url", "domain", "category"],
                          order={"uptime": 1},
                          limit=num)
    while True:
        try:
            article = cursor.next()
            r.rpush("article", json.dumps(article))
        except StopIteration:
            break
    cursor.close()
    logging.info("reset `article` success.")


def run_topic(r: Redis, db: Database, mode: str = "hot"):
    assert mode in ["hot", "all"]
    job_list = [JrjReport(), JrjNews(), SinaReport(), EastmoneyReport()]
    save_article = partial(utils.save_article, db)
    while r.exists("stock"):
        code = r.lpop("stock").decode()
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
    save_article = partial(utils.save_article, db)
    while r.exists("article"):
        article = json.loads(r.lpop("article").decode())
        url = article.get("url")
        logging.info("start article {}...".format(url))
        # noinspection PyProtectedMember
        for k in set(article.keys()).difference(Article._fields):
            del article[k]
            article = Article(**article)
        job_type = article.domain + "_" + article.category
        job = job_map.get(job_type)
        if job:
            article = job.get_article_detail(article)
            column = column_map[job_type]
            # noinspection PyProtectedMember
            save_article(article._asdict(), column)
            logging.info("save article success. url: {}".format(url))
    logging.info("job complete.")

