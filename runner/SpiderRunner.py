import datetime
import json
import logging
import traceback
from logging.handlers import RotatingFileHandler

import pymongo

from conn.client import mongodb_client, redis_client
from runner.config import STOCK_KEY, STOCKS, ARTICLE_TABLE, TOPIC_KEY, INFO_TABLE, FINANCE_TABLE, MARKET_TABLE, \
    MARKET_KEY, DATE_KEY, BASIC_KEY
from spider.website import WebSite
from spider.market import Market

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
    # mongodb
    article_table = ARTICLE_TABLE
    info_table = INFO_TABLE
    finance_table = FINANCE_TABLE
    market_table = MARKET_TABLE
    # redis
    stock_key = STOCK_KEY
    topic_key = TOPIC_KEY
    date_key = DATE_KEY
    market_key = MARKET_KEY
    basic_key = BASIC_KEY

    def __init__(self):
        pass

    def get_stock_left(self) -> list:
        return self.r.lrange(self.stock_key, 0, 5000)

    def get_topic_left(self) -> list:
        return self.r.lrange(self.topic_key, 0, 5000)

    def clear_stock(self) -> None:
        """
        清空redis中的stock队列
        :return:
        """
        logger.info("start clear stock")
        self.r.delete(self.stock_key)
        logger.info("clear stock success.")

    def reset_stock(self) -> None:
        """
        重置redis中的stock队列 [code,code,...]
        :return:
        """
        logger.info("start reset stock")
        self.r.delete(self.stock_key)
        self.r.rpush(self.stock_key, *STOCKS)
        logger.info("reset stock success.")

    def clear_topic(self) -> None:
        """
        清空redis中的topic队列 [{url,domain,category},{url,domain,category},...]
        :return:
        """
        logger.info("start clear topic")
        self.r.delete(self.topic_key)
        logger.info("clear topic success.")

    def reset_topic(self) -> None:
        """
        重置redis中的topic队列[{url:,domain:,category:},{url:,domain:,category:},...]
        :return:
        """
        logger.info("start reset topic")
        self.r.delete(self.topic_key)
        cur = self.db.get_collection(self.article_table) \
            .find({"$or": [{"content": ""}, {"content": {"$exists": False}}]},
                  {"_id": 0, "url": 1, "domain": 1, "category": 1})\
            .sort([("uptime", pymongo.ASCENDING)])\
            .limit(10000)
        for article in cur:
            self.r.rpush(self.topic_key, json.dumps(article))
        logger.info("reset topic success.")

    def clear_date(self) -> None:
        """
        清空redis中的date队列
        :return:
        """
        logger.info("start clear date")
        self.r.delete(self.date_key)
        logger.info("clear date success.")

    def reset_date(self) -> None:
        """
        重置redis中的date队列 [code,code,...]
        :return:
        """
        logger.info("start reset date")
        self.r.delete(self.date_key)
        start = "20160101"
        end = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y%m%d")
        market = Market()
        dates = market.get_trade_day(start, end)
        self.r.rpush(self.date_key, *dates)
        logger.info("reset date success.")

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

    def next_date(self) -> str:
        """
        返回一个date
        :return:
        """
        data = self.r.lpop(self.date_key)
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

    def info_runner(self, website: WebSite, code: str) -> int:
        flag = 0
        tps = website.get_info(code)
        for tp in tps if tps else []:
            self.save_info(code, tp)
        flag += len(tps)
        logger.info("{} info {} records".format(code, len(tps)))
        return flag

    def finance_runner(self, website: WebSite, code: str) -> int:
        flag = 0
        tps = website.get_summary(code)
        for tp in tps if tps else []:
            self.save_finance(code, "summary", tp)
        flag += len(tps)
        logger.info("{} summary {} records".format(code, len(tps)))
        tps = website.get_balance(code)
        for tp in tps if tps else []:
            self.save_finance(code, "balance", tp)
        flag += len(tps)
        logger.info("{} balance {} records".format(code, len(tps)))
        tps = website.get_cashflow(code)
        for tp in tps if tps else []:
            self.save_finance(code, "cashflow", tp)
        flag += len(tps)
        logger.info("{} cashflow {} records".format(code, len(tps)))
        tps = website.get_profit(code)
        for tp in tps if tps else []:
            self.save_finance(code, "profit", tp)
        flag += len(tps)
        logger.info("{} profit {} records".format(code, len(tps)))
        return flag

    def save_article(self, document: dict) -> int:
        modified_count = -1
        document = {k: v for k, v in document.items() if v}
        try:
            url = document["url"]
            document["uptime"] = datetime.datetime.now().strftime("%Y-%m-%d %X")
            document = {"$set": document}
            result = self.db.get_collection(self.article_table) \
                .update_one({"url": url}, document, upsert=True)
            modified_count = result.modified_count
        except KeyError:
            traceback.print_exc()
        return modified_count

    def save_info(self, code: str, tp: tuple) -> int:
        assert len(tp) == 3
        n, v, o = tp
        document = {"code": code, "name": n, "value": v, "other": o,
                    "uptime": datetime.datetime.now().strftime("%Y-%m-%d %X")}
        document = {"$set": document}
        result = self.db.get_collection(self.info_table) \
            .update_one({"code": code, "name": n, "value": v}, document, upsert=True)
        modified_count = result.modified_count
        return modified_count

    def save_finance(self, code: str, category: str, tp: tuple) -> int:
        assert len(tp) == 3
        n, v, o = tp
        document = {"code": code, "category": category, "name": n, "value": v, "other": o,
                    "uptime": datetime.datetime.now().strftime("%Y-%m-%d %X")}
        document = {"$set": document}
        result = self.db.get_collection(self.finance_table) \
            .update_one({"code": code, "category": category, "name": n}, document, upsert=True)
        modified_count = result.modified_count
        return modified_count

    def online_runner(self) -> int:
        update_time = datetime.datetime.now().strftime("%Y-%m-%d %X")
        market = Market()
        data = market.get_online_data()
        data = {d["code"]: json.dumps(dict(**d, update_time=update_time)) for d in data}
        if data:
            self.r.delete(self.market_key)
            self.r.hmset(self.market_key, data)
        logger.info("online market {} records.".format(len(data)))
        return len(data)

    def offline_runner(self, dt: str=None) -> int:
        yesterday = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y%m%d")
        dt = yesterday if dt is None else dt
        market = Market()
        data = market.get_daily_data(dt)
        if data:
            self.db.get_collection(self.market_table).delete_many({"trade_date": dt})
            self.db.get_collection(self.market_table).insert_many(data)
        logger.info("{} offline market {} records".format(dt, len(data)))
        return len(data)

    def basic_runner(self) -> int:
        update_time = datetime.datetime.now().strftime("%Y-%m-%d %X")
        market = Market()
        data = market.get_basic_data()
        data = {d["code"]: json.dumps(dict(**d, update_time=update_time)) for d in data}
        if data:
            self.r.delete(self.basic_key)
            self.r.hmset(self.basic_key, data)
        logger.info("basic {} records.".format(len(data)))
        return len(data)


if __name__ == '__main__':
    from spider.websites import sina

    job = SpiderRunner()
    # job.topic_runner(sina.SinaReport(), "600597")
    # print(job.offline_runner("20190103"))
    # print(job.online_runner())
    job.basic_runner()
