from spider.job.client import get_zookeeper_client
from spider.job.config import zookeeper_root
from decorator import decorator
import logging
import socket
import os


# 唯一任务 节点 计算机名称|进程号 有记录则不执行
def register_single_job(node=""):
    @decorator
    def wrap(func, *args, **kwargs):
        zk = get_zookeeper_client()
        node_path = "/".join([zookeeper_root, node])
        ret = None
        if not zk.exists(node_path) or not zk.get_children(node_path):
            v = "|".join([socket.gethostname(), str(os.getpid())])
            logging.info("job start. node: {} add {}".format(node_path, v))
            zk.create(path=node_path+"/"+v, value=b"running", ephemeral=True, makepath=True)
            ret = func(*args, **kwargs)
        zk.stop()
        zk.close()
        return ret

    return wrap


# 并行任务 增加节点 计算机名|进程号 value 记录 running
def register_multiple_job(node=""):
    @decorator
    def wrap(func, *args, **kwargs):
        zk = get_zookeeper_client()
        node_path = "/".join([zookeeper_root, node])
        v = "|".join([socket.gethostname(), str(os.getpid())])
        logging.info("job start. node: {} add {}".format(node_path, v))
        zk.create(path=node_path + "/" + v, value=b"running", ephemeral=True, makepath=True)
        ret = func(*args, **kwargs)
        zk.stop()
        zk.close()
        return ret

    return wrap
