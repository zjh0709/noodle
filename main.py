import argparse
from command.spider import reset_article, reset_topic, run_article, run_topic
from command.manager import job_list, job_kill


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--job", dest="job", default=None)
    parser.add_argument("--sub", dest="sub", default=None)
    parser.add_argument("--parm", dest="parm", default=None)
    args = parser.parse_args()
    if args.job == "spider" and args.sub == "reset_topic":
        reset_topic()
    elif args.job == "spider" and args.sub == "topic":
        run_topic(mode="hot")
    elif args.job == "spider" and args.sub == "topic_all":
        run_topic(mode="all")
    elif args.job == "spider" and args.sub == "reset_article":
        reset_article()
    elif args.job == "spider" and args.sub == "article":
        run_article()
    elif args.job == "manager" and args.sub == "list" and args.parm:
        job_list(args.parm)
    elif args.job == "manager" and args.sub == "kill" and args.parm:
        job_kill(args.parm)
