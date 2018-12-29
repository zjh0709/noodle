from spider.job.zoo import register_single_job, register_multiple_job
from spider.job import crawl, client


@register_single_job(node="spider/reset_topic")
def reset_topic():
    r = client.get_redis_client()
    crawl.reset_topic(r)


@register_single_job(node="spider/reset_article")
def reset_article(num=1000):
    r = client.get_redis_client()
    db = client.get_mongodb_database()
    crawl.reset_article(r, db, num)
    db.client.close()


@register_multiple_job(node="spider/run_topic")
def run_topic(mode="hot"):
    r = client.get_redis_client()
    db = client.get_mongodb_database()
    crawl.run_topic(r, db, mode)
    db.client.close()


@register_multiple_job(node="spider/run_article")
def run_article():
    r = client.get_redis_client()
    db = client.get_mongodb_database()
    crawl.run_article(r, db)
    db.client.close()

