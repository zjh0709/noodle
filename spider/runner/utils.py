import logging

from pymongo.database import Database
from pymongo.cursor import Cursor
import datetime

from redis import Redis


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
        result = db.get_collection(table).update_one({"url": url}, document, upsert=True)
        modified_count = result.modified_count
    return modified_count


def save_info(db: Database, table: str, document: dict) -> int:
    uptime = datetime.datetime.now().strftime("%Y-%m-%d %X")
    document.setdefault("uptime", uptime)
    code = document.get("code")
    name = document.get("name")
    value = document.get("value")
    modified_count = 0
    if code and name and value:
        document = {"$set": document}
        result = db.get_collection(table).update_one({"code": code, "name": name, "value": value}, document, upsert=True)
        modified_count = result.modified_count
    return modified_count


def save_word(db: Database, table: str, document: dict) -> int:
    uptime = datetime.datetime.now().strftime("%Y-%m-%d %X")
    document.setdefault("uptime", uptime)
    code = document.get("code")
    word = document.get("word")
    modified_count = 0
    if code and word:
        document = {"$set": document}
        result = db.get_collection(table).update_one({"code": code, "word": word}, document, upsert=True)
        modified_count = result.modified_count
    return modified_count


def load_document(db: Database, table: str, spec: dict = {}, column: list = [],
                  order: dict = {}, limit: int = None) -> Cursor:
    column = {c: 1 for c in column}
    column.update({"_id": 0})
    cur = db.get_collection(table).find(spec, column)
    if order:
        cur = cur.sort(list(order.items()))
    if limit:
        cur = cur.limit(limit=limit)
    return cur


def reset_key(r: Redis, k: str):
    logging.info("start reset `{}`...".format(k))
    if r.exists(k) > 0:
        logging.warning("key `{}` is exists. will delete it.".format(k))
        r.delete(k)
        logging.info("delete key `{}` success.".format(k))
