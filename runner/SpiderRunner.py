import datetime
import json
import logging
import traceback

from logging.handlers import RotatingFileHandler

from conn.client import mongodb_client, redis_client
from runner.config import STOCK_KEY, STOCKS, ARTICLE_TABLE, TOPIC_KEY
from spider.website import WebSite

console = RotatingFileHandler(filename="/mnt/d/log/noodle/spider.log",
                              mode="a",
                              maxBytes=100*1024*1024,
                              backupCount=3)
console.setFormatter(logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(console)


class SpiderRunner(object):
    db = mongodb_client()
    r = redis_client()
    table = ARTICLE_TABLE
    stock_key = STOCK_KEY
    topic_key = TOPIC_KEY

    def __init__(self):
        pass

    def get_stock_len(self) -> int:
        return self.r.llen(self.stock_key)

    def get_topic_len(self) -> int:
        return self.r.llen(self.topic_key)

    def reset_stock(self) -> None:
        """
        重置redis中的stock队列 [url,url,...]
        :return:
        """
        logger.info("start reset stock")
        self.r.delete(self.stock_key)
        self.r.rpush(self.stock_key, *STOCKS)
        logger.info("reset stock success.")

    def reset_topic(self) -> None:
        """
        重置redis中的article队列[{url:,domain:,category:},{url:,domain:,category:},...]
        :return:
        """
        logger.info("start reset topic")
        self.r.delete(self.topic_key)
        cur = self.db.get_collection(self.table) \
            .find({"$or": [{"content": ""}, {"content": {"$exists": False}}]},
                  {"_id": 0, "url": 1, "domain": 1, "category": 1}).limit(5000)
        for article in cur:
            self.r.rpush(self.topic_key, json.dumps(article))
        logger.info("reset topic success.")

    def next_stock(self) -> str:
        """
        返回一个stock
        :return:
        """
        data = self.r.lpop(self.stock_key)
        return data.decode("utf-8") if data else None

    def next_topic(self) -> str:
        """
        返回一个topic
        :return:
        """
        data = self.r.lpop(self.topic_key)
        return data.decode("utf-8") if data else None

    def topic_runner(self, website: WebSite, code: str, mode: str = "append") -> int:
        """
        跑topic
        :param code:
        :param mode:
        :param website:
        :return:
        """
        assert mode in ("append", "overwrite")
        if mode == "append":
            page = website.first_page(code)
            topics = website.get_topics_by_page(page)
        else:
            topics = website.get_topics_by_code(code)
        for topic in topics:
            self.save_article(topic)
            logger.info("{} {}".format(code, topic.get("title", "")))
        flag = len(topics)
        return flag

    def article_runner(self, website: WebSite, topic: str) -> int:
        flag = 0
        try:
            topic = json.loads(topic)
            if topic["domain"] == website.domain and \
                    topic["category"] == website.category:
                article = website.get_article_detail(topic)
                self.save_article(article)
                logger.info("{} {}".format(article["domain"], article["category"]))
                flag = 1
        except json.decoder.JSONDecodeError:
            traceback.print_exc()
        except KeyError:
            traceback.print_exc()
        return flag

    def save_article(self, document: dict) -> int:
        modified_count = -1
        document = {k: v for k, v in document.items() if v}
        try:
            url = document["url"]
            document["uptime"] = datetime.datetime.now().strftime("%Y-%m-%d %X")
            document = {"$set": document}
            result = self.db.get_collection(self.table) \
                .update_one({"url": url}, document, upsert=True)
            modified_count = result.modified_count
        except KeyError:
            traceback.print_exc()
        return modified_count


if __name__ == '__main__':
    from spider.websites import sina

    job = SpiderRunner()
    job.topic_runner(sina.SinaReport(), "600597")
