from conn.client import zookeeper_client
from conn.config import zookeeper_root

from decorator import decorator
import logging
import socket
import os


# 唯一任务 节点 计算机名称_进程号 有记录则不执行
def register_single_job(node=""):
    @decorator
    def wrap(func, *args, **kwargs):
        zk = zookeeper_client()
        node_path = "/".join([zookeeper_root, node])
        ret = None
        if not zk.exists(node_path) or not zk.get_children(node_path):
            v = "_".join([socket.gethostname(), str(os.getpid())])
            logging.info("job start. node: {} add {}".format(node_path, v))
            zk.create(path=node_path+"/"+v, value=b"running", ephemeral=True, makepath=True)
            ret = func(*args, **kwargs)
        zk.stop()
        zk.close()
        return ret

    return wrap


# 并行任务 增加节点 计算机名_进程号 value 记录 running
def register_multiple_job(node=""):
    @decorator
    def wrap(func, *args, **kwargs):
        zk = zookeeper_client()
        node_path = "/".join([zookeeper_root, node])
        v = "_".join([socket.gethostname(), str(os.getpid())])
        logging.info("job start. node: {} add {}".format(node_path, v))
        zk.create(path=node_path + "/" + v, value=b"running", ephemeral=True, makepath=True)
        ret = func(*args, **kwargs)
        zk.stop()
        zk.close()
        return ret

    return wrap


def get_node_path(node: str):
    return "/".join([zookeeper_root, node])


def add_node(node: str="", v: str=""):
    zk = zookeeper_client()
    node_path = "/".join([zookeeper_root, node])
    zk.create(path=node_path + "/" + v, value=b"running", ephemeral=True, makepath=True)
    zk.stop()
    zk.close()
