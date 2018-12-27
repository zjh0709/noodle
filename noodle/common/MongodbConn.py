import pymongo
from noodle.common.config import mongodb_host, mongodb_port


class MongodbConn(object):

    def __init__(self):
        self.client = None

    def start(self):
        self.client = pymongo.MongoClient(host=mongodb_host, port=mongodb_port)

    def stop(self):
        self.client.close()

