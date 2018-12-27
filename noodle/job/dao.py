import datetime
import traceback
from pymongo.cursor import Cursor

from noodle.common.client import get_mongodb_client
from noodle.scrapy.entity import Article


class Dao(object):

    def __init__(self):
        self.client = get_mongodb_client()
        self.db = self.client.get_database("noodle")

    def save_article(self, article: Article, column: list=None) -> int:
        # noinspection PyBroadException
        try:
            uptime = datetime.datetime.now().strftime("%Y-%m-%d %X")
            # noinspection PyProtectedMember
            document = dict(article._asdict())
            if column:
                for k in set(document.keys()).difference(column):
                    document.__delitem__(k)
            document.setdefault("uptime", uptime)
            document = {"$set": document}
            self.db.get_collection("article").update(spec={"url": article.url},
                                                     document=document,
                                                     upsert=True)
            return 1
        except Exception:
            traceback.print_exc()
            return 0

    def load_article(self, spec: dict = {}, column: list = [],
                     order: dict = {}, limit: int = None) -> Cursor:
        column = {c: 1 for c in column}
        column.update({"_id": 0})
        data = self.db.get_collection("article").find(spec, column)
        if order:
            data = data.sort(list(order.items()))
        if limit:
            data = data.limit(limit=limit)
        return data

    @staticmethod
    def dict_to_article(data_: dict) -> Article:
        # noinspection PyProtectedMember
        for k in set(data_.keys()).difference(Article._fields):
            data_.__delitem__(k)
        return Article(**data_)


if __name__ == '__main__':
    data = {"url": "aaa", "code": "555", "hello": "hehe"}
    print(Dao.dict_to_article(data))
