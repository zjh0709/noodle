import json

from noodle.scrapy.website.sina import SinaReport
from noodle.scrapy.website.jrj import JrjReport, JrjNews
from noodle.scrapy.website.eastmoney import EastmoneyReport

import logging

from noodle.common.config import stock
from noodle.job.dao import Dao
from noodle.common.client import get_redis_client


def reset_topic():
    logging.info("start reset stock...")
    r = get_redis_client()
    if r.exists("stock") > 0:
        logging.warning("key `stock` is exists. will delete it.")
        r.delete("stock")
        logging.info("delete key `stock` success.")
    r.rpush("stock", *stock)
    logging.info("reset stock success.")


def reset_article():
    logging.info("start restart article...")
    r = get_redis_client()
    if r.exists("article") > 0:
        logging.warning("key `article` is exists. will delete it.")
        r.delete("article")
        logging.info("delete key `article` success.")
    dao = Dao()
    cursor = dao.load_article(spec={"content": ""}, column=["url", "domain", "category"],
                              order={"uptime": 1}, limit=1000)
    while True:
        try:
            article = cursor.next()
            r.rpush("article", json.dumps(article))
        except StopIteration:
            break
    cursor.close()


def run_topic(mode: str = "hot"):
    assert mode in ["hot", "all"]
    r = get_redis_client()
    dao = Dao()
    job_list = [JrjReport(), JrjNews(), SinaReport(), EastmoneyReport()]
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
                dao.save_article(article)
        logging.info("stock {} success.".format(code))
    logging.info("job complete.")
    dao.client.close()


def run_article():
    r = get_redis_client()
    dao = Dao()
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
    while r.exists("article"):
        article = json.loads(r.lpop("article").decode())
        url = article.get("url")
        logging.info("start article {}...".format(url))
        article = Dao.dict_to_article(article)
        job_type = article.domain + "_" + article.category
        job = job_map.get(job_type)
        if job:
            article = job.get_article_detail(article)
            column = column_map[job_type]
            dao.save_article(article, column)
            logging.info("save article success. url: {}".format(url))


if __name__ == '__main__':
    reset_article()
    run_article()
