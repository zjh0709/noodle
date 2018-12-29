from pymongo.database import Database
from pymongo.cursor import Cursor
import datetime


def save_article(db: Database, document: dict, column: list = None) -> int:
    uptime = datetime.datetime.now().strftime("%Y-%m-%d %X")
    if column:
        for k in set(document.keys()).difference(column):
            del document[k]
    document.setdefault("uptime", uptime)
    document = {"$set": document}
    db.get_collection("article") \
        .update(spec={"url": document.get("url", "")},
                document=document,
                upsert=True)


def load_article(db: Database, spec: dict = {}, column: list = [],
                 order: dict = {}, limit: int = None) -> Cursor:
    column = {c: 1 for c in column}
    column.update({"_id": 0})
    cur = db.get_collection("article").find(spec, column)
    if order:
        cur = cur.sort(list(order.items()))
    if limit:
        cur = cur.limit(limit=limit)
    return cur
