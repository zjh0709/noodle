from decorator import decorator
from conn.client import zookeeper_client
from conn.config import zookeeper_root
import socket
import os


def register_job():
    @decorator
    def wrap(func, *args, **kwargs):
        zk = zookeeper_client()
        node = zookeeper_root + func.__name__
        zk.create(path=node, value="{}_{}".format(socket.gethostname(), os.getpid()).encode(),
                  ephemeral=True, sequence=True, makepath=True)
        return func(*args, **kwargs)
    return wrap


def get_jobs(name: str):
    zk = zookeeper_client()
    jobs = {child: zk.get(zookeeper_root + child)[0] for
            child in zk.get_children(zookeeper_root) if name in child}
    zk.stop()
    zk.close()
    return jobs


def get_jobs_all():
    zk = zookeeper_client()
    jobs = {child: zk.get(zookeeper_root + child)[0] for
            child in zk.get_children(zookeeper_root)}
    zk.stop()
    zk.close()
    return jobs


if __name__ == '__main__':
    @register_job()
    def demo():
        import time
        time.sleep(10)
        print("hello")
    demo()
