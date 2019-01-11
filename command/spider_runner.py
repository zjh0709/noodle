from conn import utils as conn_utils
from spider.runner import crawler, extractor, resetter
from conn import client


@conn_utils.register_single_job(node="spider/reset_stock")
def reset_stock():
    r = client.redis_client()
    resetter.reset_stock(r)


@conn_utils.register_single_job(node="spider/reset_topic")
def reset_topic(num=1000):
    r = client.redis_client()
    db = client.mongodb_client()
    resetter.reset_topic(r, db, num)
    db.client.close()


@conn_utils.register_single_job(node="spider/reset_keyword")
def reset_keyword(num=1000):
    r = client.redis_client()
    db = client.mongodb_client()
    extractor.reset_keyword(r, db, num)
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


@conn_utils.register_multiple_job(node="spider/run_keyword")
def run_keyword():
    r = client.redis_client()
    db = client.mongodb_client()
    extractor.run_keyword(r, db)
    db.client.close()


@conn_utils.register_multiple_job(node="spider/run_info")
def run_info():
    r = client.redis_client()
    db = client.mongodb_client()
    crawler.run_info(r, db)
    db.client.close()


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    reset_topic()
    run_info()

