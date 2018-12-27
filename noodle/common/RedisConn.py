import redis
from noodle.common.config import redis_host, redis_port

class RedisConn(object):

    def __init__(self):
        self.r = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.r.set