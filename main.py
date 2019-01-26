import logging

import sys

from quartz.SpiderQuartz import SpiderScheduler
from script import spider_script

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd == "start":
        spider_scheduler = SpiderScheduler()
        spider_scheduler.start()
    elif cmd == "reset":
        spider_script.reset_stock()
    elif cmd == "all":
        spider_script.run_topic("overwrite")
