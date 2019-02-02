import sys

from quartz.SpiderQuartz import SpiderScheduler
from quartz.ModelQuartz import ModelQuartz
from script import spider_script


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd == "start1":
        spider_scheduler = SpiderScheduler()
        spider_scheduler.start()
    elif cmd == "start2":
        model_scheduler = ModelQuartz()
        model_scheduler.start()
    elif cmd == "reset":
        spider_script.reset_stock()
    elif cmd == "topic":
        spider_script.run_topic()
    elif cmd == "all":
        spider_script.run_topic("overwrite")
    elif cmd == "article":
        spider_script.run_article()
    elif cmd == "finance":
        spider_script.run_finance()
    elif cmd == "info":
        spider_script.run_info()
