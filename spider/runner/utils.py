from pymongo.database import Database
from pymongo.cursor import Cursor
import datetime


def save_article(db: Database, table: str, document: dict, column: list = None) -> int:
    uptime = datetime.datetime.now().strftime("%Y-%m-%d %X")
    if column:
        for k in set(document.keys()).difference(column):
            del document[k]
    document.setdefault("uptime", uptime)
    url = document.get("url")
    modified_count = 0
    if url:
        document = {"$set": document}
        result = db.get_collection(table).replace_one({"url": url}, document, upsert=True)
        modified_count = result.modified_count
    return modified_count


def load_article(db: Database, table: str, spec: dict = {}, column: list = [],
                 order: dict = {}, limit: int = None) -> Cursor:
    column = {c: 1 for c in column}
    column.update({"_id": 0})
    cur = db.get_collection(table).find(spec, column)
    if order:
        cur = cur.sort(list(order.items()))
    if limit:
        cur = cur.limit(limit=limit)
    return cur


