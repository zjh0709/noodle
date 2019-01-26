import logging

from kazoo.client import KazooClient
from kazoo.handlers.threading import KazooTimeoutError
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError
from redis import Redis

from conn.config import mongodb_host, mongodb_port, mongodb_database, redis_host, redis_port, zookeeper_host


def mongodb_client() -> Database:
    client = MongoClient(host=mongodb_host, port=mongodb_port)
    try:
        logging.debug("mongodb info:")
        # logging.info(client.server_info())
        client = client.get_database(mongodb_database)
    except ServerSelectionTimeoutError:
        logging.warning("connect to mongodb error.")
        client = None
    return client


def redis_client() -> Redis:
    client = Redis(host=redis_host, port=redis_port)
    try:
        logging.debug("redis info:")
        # logging.info(client.info())
    except ConnectionError:
        logging.warning("connect to redis error.")
        client = None
    return client


def zookeeper_client() -> KazooClient:
    client = KazooClient(hosts=zookeeper_host)
    try:
        client.start(timeout=10)
        logging.debug("zookeeper info:")
        # logging.info(client.server_version())
    except KazooTimeoutError:
        logging.warning("connect to zookeeper error.")
        client = None
    return client
