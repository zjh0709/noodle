import os
import signal
import socket
import logging
import traceback

from conn.client import zookeeper_client
from conn.utils import get_node_path


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
    children = []
    if zk.exists(node_path):
        children = zk.get_children(node_path)
    for child in children:
        job = zk.get_children(node_path + "/" + child)
        for j in job:
            print("{} {}".format(children, j))
    zk.stop()
    zk.close()

