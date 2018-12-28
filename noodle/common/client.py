from pymongo.mongo_client import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from redis.client import Redis
from redis.exceptions import ConnectionError
from kazoo.client import KazooClient
from kazoo.handlers.threading import KazooTimeoutError

from noodle.common.config import mongodb_port, mongodb_host
from noodle.common.config import redis_port, redis_host
from noodle.common.config import zookeeper_host

import logging


def get_mongodb_client() -> MongoClient:
    client = MongoClient(host=mongodb_host, port=mongodb_port)
    try:
        logging.info("mongodb info:")
        logging.info(client.server_info())
    except ServerSelectionTimeoutError:
        logging.warning("connect to mongodb error.")
        exit(0)
    return client


def get_redis_client() -> Redis:
    client = Redis(host=redis_host, port=redis_port)
    try:
        logging.info("redis info:")
        logging.info(client.info())
    except ConnectionError:
        logging.warning("connect to redis error.")
        exit(0)
    return client


def get_zookeeper_client() -> KazooClient:
    client = KazooClient(hosts=zookeeper_host)
    try:
        client.start(timeout=10)
        logging.info("zookeeper info:")
        logging.info(client.server_version())
    except KazooTimeoutError:
        logging.warning("connect to zookeeper error.")
        exit(0)
    return client


if __name__ == '__main__':
    c = get_zookeeper_client()
    c.stop()
    c.close()
