import datetime
import logging
import traceback
from logging.handlers import RotatingFileHandler

import pymongo

from conn.client import mongodb_client, redis_client
from model.nlp import Nlp
from runner.config import ARTICLE_TABLE, INFO_TABLE, KEYWORD_KEY

console = RotatingFileHandler(filename="/mnt/d/log/noodle/model.log",
                              mode="a",
                              maxBytes=100 * 1024 * 1024,
                              backupCount=3)
console.setFormatter(logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(console)


class ModelRunner(object):
    db = mongodb_client()
    r = redis_client()
    # mongodb
    article_table = ARTICLE_TABLE
    info_table = INFO_TABLE
    # redis
    keyword_key = KEYWORD_KEY

    def __init__(self):
        pass

    def get_keyword_left(self) -> list:
        return self.r.lrange(self.keyword_key, 0, 5000)

    def clear_keyword(self) -> None:
        """
        清空redis中的keyword队列
        :return:
        """
        logger.info("start clear keyword")
        self.r.delete(self.keyword_key)
        logger.info("clear keyword success.")

    def reset_keyword(self) -> None:
        """
        重置redis中的keyword队列 [url,url,...]
        :return:
        """
        logger.info("start reset keyword")
        self.r.delete(self.keyword_key)
        cur = self.db.get_collection(self.article_table) \
            .find({"content": {"$exists": True, "$ne": ""}, "keyword": {"$exists": False}},
                  {"_id": 0, "url": 1}) \
            .sort([("uptime", pymongo.ASCENDING)]) \
            .limit(5000)
        for article in cur:
            self.r.rpush(self.keyword_key, article["url"])
        logger.info("reset keyword success.")

    def next_keyword(self) -> str:
        """
        返回一个topic
        :return:
        """
        data = self.r.lpop(self.keyword_key)
        return data.decode("utf-8") if data else None

    def keyword_runner(self, nlp: Nlp, url: str) -> int:
        """
        跑keyword
        :param nlp:
        :param url:
        :return:
        """
        article = self.db.get_collection(self.article_table) \
            .find_one({"url": url},
                      {"_id": 0, "url": 1, "title": 1, "content": 1, "code": 1})
        keywords = nlp.keyword(title=article.get("title", ""), content=article.get("content", ""))
        logger.info("{} {}".format(article.get("code"), " ".join(keywords)))
        try:
            del article["content"]
        except KeyError:
            traceback.print_exc()
        article["keyword"] = keywords
        self.save_article(article)
        return len(keywords)

    def save_article(self, document: dict) -> int:
        modified_count = -1
        document = {k: v for k, v in document.items() if v}
        try:
            url = document["url"]
            document["uptime"] = datetime.datetime.now().strftime("%Y-%m-%d %X")
            document = {"$set": document}
            result = self.db.get_collection(self.article_table) \
                .update_one({"url": url}, document, upsert=False)
            modified_count = result.modified_count
        except KeyError:
            traceback.print_exc()
        return modified_count


if __name__ == '__main__':
    from model.NlpModel import baidu

    job = ModelRunner()
    job.keyword_runner(baidu.BaiduNlp(),
                       "http://vip.stock.finance.sina.com.cn/q/go.php/vReport_Show/kind/search/rptid/3614495/index.phtml")
