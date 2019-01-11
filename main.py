import sys

from command.spider_runner import reset_stock, reset_topic, reset_keyword
from command.spider_runner import run_article, run_topic, run_keyword
from command.spider_manager import job_list, job_kill, job_check

if __name__ == '__main__':
    p1 = sys.argv[1] if len(sys.argv) > 1 else None
    p2 = sys.argv[2] if len(sys.argv) > 2 else None
    p3 = sys.argv[3] if len(sys.argv) > 3 else None
    if p1 == "reset":
        if p2 == "stock":
            reset_stock()
        elif p2 == "topic":
            num = int(p3) if str(p3).isdecimal() else 5000
            reset_topic(num=num)
        elif p2 == "keyword":
            num = int(p3) if str(p3).isdecimal() else 5000
            reset_keyword(num=num)
    elif p1 == "topic":
        if p2 == "all":
            run_topic(mode="all")
        else:
            run_topic(mode="hot")
    elif p1 == "article":
        run_article()
    elif p1 == "keyword":
        run_keyword()
    elif p1 == "list" and p2:
        job_list(p2)
    elif p1 == "kill" and p2:
        job_kill(p2)
    elif p1 == "check" and p2:
        job_check(p2)
