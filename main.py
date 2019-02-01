import logging

import sys

from quartz.SpiderQuartz import SpiderScheduler
from script import spider_script

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd == "start":
        spider_scheduler = SpiderScheduler()
        spider_scheduler.start()
    elif cmd == "reset":
        spider_script.reset_stock()
    elif cmd == "all":
        spider_script.run_topic("overwrite")
    elif cmd == "finance":
        spider_script.run_finance()
    elif cmd == "info":
        spider_script.run_info()
