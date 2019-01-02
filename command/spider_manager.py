import os
import signal
import socket
import logging
import traceback

from conn.client import zookeeper_client, redis_client
from conn.utils import get_node_path
from spider.runner.config import TOPIC_KEY, STOCK_KEY


def job_kill(job_name: str):
    try:
        hostname, pid = [i[::-1] for i in job_name[::-1].split("_", 1)][::-1]
        if hostname == socket.gethostname():
            os.kill(int(pid), signal.SIGKILL)
    except ValueError:
        logging.warning("job name error. name {}.".format(job_name))
        traceback.print_exc()


def job_list(node: str):
    zk = zookeeper_client()
    node_path = get_node_path(node)
    if zk.exists(node_path):
        children = zk.get_children(node_path)
        for child in children:
            jobs = zk.get_children(node_path + "/" + child)
            for job in jobs:
                print("{} {} {}".format(node, child, job))
    zk.stop()
    zk.close()


def job_check(k: str):
    assert k in (STOCK_KEY, TOPIC_KEY)
    r = redis_client()
    print("{} count {}".format(k, r.llen(k)))

