import json

from redis.client import Redis
from pymongo.database import Database

from spider.runner.config import STOCK_KEY, TOPIC_KEY, STOCK_COMPLETE_KEY
from spider.runner.config import ARTICLE_TABLE, INFO_TABLE, WORD_TABLE
from spider.runner import utils
from spider.website.sina import SinaReport
from spider.website.jrj import JrjReport, JrjNews
from spider.website.eastmoney import EastmoneyReport
from spider.website.hexun import HexunBase

import logging

from functools import partial
from spider.entity import article_to_dict, dict_to_article


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
        r.lpush(STOCK_COMPLETE_KEY, code)
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
        "jrj_report": ["url", "content", "author", "date"],
        "jrj_news": ["url", "content", "org", "date"],
        "sina_report": ["url", "title", "content", "author", "org", "date"],
        "eastmoney_report": ["url", "content"]
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
            modified_count = save_article(article, column)
            if modified_count > 0:
                logging.info("save article success. url: {}".format(url))
            else:
                logging.info("save article failed. url: {}".format(url))
    logging.info("job complete.")


def run_info(r: Redis, db: Database):
    hexun_base = HexunBase()
    save_info = partial(utils.save_info, db, INFO_TABLE)
    save_word = partial(utils.save_word, db, WORD_TABLE)
    while r.exists(STOCK_KEY):
        code = r.lpop(STOCK_KEY).decode()
        # hexun
        info = hexun_base.get_info(code)
        for k, v in info.items():
            save_info({"code": code, "name": k, "value": v})
        for word in info.get("所属行业", []):
            save_word({"code": code, "word": word})
        for word in info.get("所属概念", []):
            save_word({"code": code, "word": word})
        logging.info("save info success. code: {}".format(code))
    logging.info("job complete.")
