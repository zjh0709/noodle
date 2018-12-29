from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError
from redis.client import Redis
from redis.exceptions import ConnectionError
from kazoo.client import KazooClient
from kazoo.handlers.threading import KazooTimeoutError

from spider.job.config import mongodb_port, mongodb_host, mongodb_database
from spider.job.config import redis_port, redis_host
from spider.job.config import zookeeper_host

import logging


def get_mongodb_client() -> MongoClient:
    client = MongoClient(host=mongodb_host, port=mongodb_port)
    try:
        logging.info("mongodb info:")
        # logging.info(client.server_info())
    except ServerSelectionTimeoutError:
        logging.warning("connect to mongodb error.")
        client = None
    return client


def get_mongodb_database() -> Database:
    client = get_mongodb_client()
    return client.get_database(mongodb_database)


def get_redis_client() -> Redis:
    client = Redis(host=redis_host, port=redis_port)
    try:
        logging.info("redis info:")
        # logging.info(client.info())
    except ConnectionError:
        logging.warning("connect to redis error.")
        client = None
    return client


def get_zookeeper_client() -> KazooClient:
    client = KazooClient(hosts=zookeeper_host)
    try:
        client.start(timeout=10)
        logging.info("zookeeper info:")
        # logging.info(client.server_version())
    except KazooTimeoutError:
        logging.warning("connect to zookeeper error.")
        client = None
    return client


if __name__ == '__main__':
    c = get_mongodb_client()
    db = c.get_database("noodle")
    print(type(db))
