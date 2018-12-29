from spider.job.client import get_zookeeper_client
from spider.job.config import zookeeper_root
from decorator import decorator
import logging
import socket
import os


def register_single_job(node=""):
    @decorator
    def wrap(func, *args, **kwargs):
        zk = get_zookeeper_client()
        node_path = "/".join([zookeeper_root, node])
        ret = None
        if zk.exists(node_path):
            logging.warning("job is running. node: {}".format(node_path))
        else:
            logging.warning("job start. node: {}".format(node_path))
            zk.create(path=node_path, value=b"running", ephemeral=True, makepath=True)
            ret = func(*args, **kwargs)
        zk.stop()
        zk.close()
        return ret
    return wrap


def register_multiple_job(node=""):
    @decorator
    def wrap(func, *args, **kwargs):
        zk = get_zookeeper_client()
        node_path = "/".join([zookeeper_root, node, socket.gethostname(), str(os.getpid())])
        logging.warning("job start. node: {}".format(node_path))
        zk.create(path=node_path, value=b"running", ephemeral=True, makepath=True)
        ret = func(*args, **kwargs)
        zk.stop()
        zk.close()
        return ret
    return wrap


@register_multiple_job(node="test")
def f(a, b):
    import time
    time.sleep(10)
    return a+b


if __name__ == '__main__':
    print(f(2, 3))
