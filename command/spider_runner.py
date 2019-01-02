from conn import utils as conn_utils
from spider.runner import crawler
from conn import client


@conn_utils.register_single_job(node="spider/reset_topic")
def reset_topic():
    r = client.redis_client()
    crawler.reset_topic(r)


@conn_utils.register_single_job(node="spider/reset_article")
def reset_article(num=1000):
    r = client.redis_client()
    db = client.mongodb_client()
    crawler.reset_article(r, db, num)
    db.client.close()


@conn_utils.register_multiple_job(node="spider/run_topic")
def run_topic(mode="hot"):
    r = client.redis_client()
    db = client.mongodb_client()
    crawler.run_topic(r, db, mode)
    db.client.close()


@conn_utils.register_multiple_job(node="spider/run_article")
def run_article():
    r = client.redis_client()
    db = client.mongodb_client()
    crawler.run_article(r, db)
    db.client.close()


if __name__ == '__main__':
    reset_topic()
