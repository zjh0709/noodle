from spider.job.config import zookeeper_root
from spider.job.client import get_zookeeper_client
import os
import signal
import socket
import logging
import traceback


def job_kill(job_name: str):
    try:
        hostname, pid = job_name.split("|", 1)
        if hostname == socket.gethostname():
            os.kill(int(pid), signal.SIGKILL)
    except ValueError:
        logging.warning("job name error. name {}.".format(job_name))
        traceback.print_exc()


def job_list(node: str):
    zk = get_zookeeper_client()
    node_path = "/".join([zookeeper_root, node])
    children = []
    if zk.exists(node_path):
        children = zk.get_children(node_path)
    zk.stop()
    zk.close()
    for job_name in children:
        print(job_name)


