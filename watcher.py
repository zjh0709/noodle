from kazoo.recipe.watchers import ChildrenWatch
from kazoo.protocol.states import WatchedEvent

from spider.job.client import get_zookeeper_client
from spider.job.config import zookeeper_root
import os
import socket
import signal


def _job_killer(pid):
    os.kill(pid, signal.SIGKILL)


def _get_nodes_value(nodes: list):
    zk = get_zookeeper_client()


def _stop_single_job(value, stat, event):
    pass


def _stop_multiple_job(children: list, event: WatchedEvent):
    pass


def start_watcher():
    zk = get_zookeeper_client()
    for node in ["spider/reset_topic",
                 "spider/reset_article",
                 "spider/run_topic",
                 "spider/run_article"]:
        zk_node = "/".join([zookeeper_root, node])
        ChildrenWatch(zk, zk_node, _stop_multiple_job, send_event=True)


if __name__ == '__main__':
    zk_ = get_zookeeper_client()

    ChildrenWatch(zk_, "/noodle", _stop_multiple_job, send_event=True)
    input()
    # (b'1', ZnodeStat(czxid=1395, mzxid=1398, ctime=1546070156874, mtime=1546070194855, version=2, cversion=0, aversion=0, ephemeralOwner=0, dataLength=1, numChildren=0, pzxid=1395), None)
    # (['spider', 'ttt'], WatchedEvent(type='CHILD', state='CONNECTED', path='/noodle'))
