import pymongo
import redis

from noodle.common.config import mongodb_port, mongodb_host
from noodle.common.config import redis_port, redis_host


def get_mongodb_client():
    return pymongo.MongoClient(host=mongodb_host, port=mongodb_port)


def get_redis_client():
    return redis.Redis(host=redis_host, port=redis_port)


if __name__ == '__main__':
    m = get_mongodb_client()
    print(m.database_names())