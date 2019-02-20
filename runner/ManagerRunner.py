import datetime

import pandas as pd
import logging
import traceback
from logging.handlers import RotatingFileHandler
from operator import itemgetter
from itertools import chain, groupby, product

import pymongo

from conn.client import mongodb_client, redis_client
from model.nlp import Nlp
from runner.config import ARTICLE_TABLE, INFO_TABLE, KEYWORD_KEY, WORD_TABLE, BASIC_KEY, MARKET_KEY, MARKET_TABLE
from spider.market import Market

console = RotatingFileHandler(filename="/mnt/d/log/noodle/manager.log",
                              mode="a",
                              maxBytes=100 * 1024 * 1024,
                              backupCount=3)
console.setFormatter(logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(console)


class ManagerRunner(object):
    db = mongodb_client()
    r = redis_client()
    # mongodb
    article_table = ARTICLE_TABLE
    info_table = INFO_TABLE
    word_table = WORD_TABLE
    market_table = MARKET_TABLE
    # redis
    keyword_key = KEYWORD_KEY
    basic_key = BASIC_KEY
    market_key = MARKET_KEY

    def __init__(self):
        pass

    def get_useful_words(self, skip: int = 0, num: int = 100) -> list:
        words = self.db.get_collection(self.word_table) \
            .find({"code.0": {"$exists": True}},
                  {"_id": 0, "word": 1}) \
            .skip(skip).limit(num)
        return [d["word"] for d in words]

    def get_useless_words(self, skip: int = 0, num: int = 100) -> list:
        words = self.db.get_collection(self.word_table) \
            .find({"score": -1},
                  {"_id": 0, "word": 1}) \
            .skip(skip).limit(num)
        return [d["word"] for d in words]

    def add_useless_word(self, word: str) -> int:
        result = self.db.get_collection(self.word_table) \
            .replace_one({"word": word},
                         {"word": word, "score": -1}, upsert=True)
        logger.info("add useless word {} success.".format(word))
        return result.modified_count

    def remove_useless_word(self, word: str) -> int:
        articles = self.db.get_collection(self.article_table) \
            .find({"keyword": {"$elemMatch": {"$eq": word}}, "code": {"$exists": True}},
                  {"_id": 0, "code": 1})
        codes = [d["code"] for d in articles]
        result = self.db.get_collection(self.word_table) \
            .replace_one({"word": word},
                         {"word": word, "code": codes}, upsert=True)
        logger.info("add word {} success. code count {}".format(word, len(codes)))
        return result.modified_count

    def save_article_keyword(self):
        useless_word = self.db.get_collection(self.word_table) \
            .find({"score": {"$eq": -1}},
                  {"_id": 0, "word": 1})
        useless_word = [d["word"] for d in useless_word]
        code_keyword = self.db.get_collection(self.article_table) \
            .find({"keyword.0": {"$exists": True}, "code": {"$exists": True}},
                  {"_id": 0, "code": 1, "keyword": 1})
        code_keyword = [(d["code"], list(set(d["keyword"]).difference(useless_word)))
                        for d in code_keyword]
        # noinspection PyTypeChecker
        code_keyword.sort(key=itemgetter(0))
        gp = groupby(code_keyword, key=itemgetter(0))
        code_keyword_map = {}
        for k, it in gp:
            code_keyword_map.setdefault(
                k, set(chain.from_iterable(map(itemgetter(1), it))).difference(useless_word))
        produced_data = map(lambda x, y: product([x], y), code_keyword_map.keys(), code_keyword_map.values())
        flatted_data = chain.from_iterable(produced_data)
        sorted_data = sorted(flatted_data, key=itemgetter(1))
        grouped_data = groupby(sorted_data, key=itemgetter(1))
        for k, it in grouped_data:
            codes = list(map(itemgetter(0), it))
            self.db.get_collection(self.word_table) \
                .replace_one({"word": k},
                             {"word": k, "code": codes}, upsert=True)
            logger.info("add word {} success. code count {}".format(k, len(codes)))

    def get_stock_by_word(self, word: str):
        today = datetime.datetime.now().strftime("%Y%m%d")
        market = Market()
        last_day = market.get_last_trade_day(today)
        record = self.db.get_collection(self.word_table).find({"word": word})
        codes = []
        try:
            codes = record.next().get("code", [])
        except StopIteration:
            traceback.print_exc()
        if codes:
            df = pd.DataFrame(codes, columns=["code"])
            close = list(self.db.get_collection(self.market_table)\
                .find({"trade_date": last_day}, {"_id": 0, "code": 1, "close": 1}))
            close_df = pd.DataFrame(close)
            basic = [pd.io.json.loads(d) for d in self.r.hgetall(self.basic_key).values()]
            basic_df = pd.DataFrame(basic)
            del basic_df["update_time"]
            market = [pd.io.json.loads(d) for d in self.r.hgetall(self.market_key).values()]
            market_df = pd.DataFrame(market)
            df = df.merge(basic_df, on="code") \
                .merge(market_df, on="code")\
                .merge(close_df, on="code")
            df["price"] = df["close"] * (1 + df["changepercent"]/100)
            df["circulation_market_value "] = df["price"] * df["outstanding"]
            df["market_value"] = df["price"] * df["totals"]
            df = df[["code", "name", "price", "changepercent",
                     "circulation_market_value ", "market_value",
                     "pb", "pe", "update_time"]]
            print(df)
            df.to_excel("{}.xlsx".format(word), index=False)


if __name__ == '__main__':
    runner = ManagerRunner()
    runner.get_stock_by_word("赛马")
