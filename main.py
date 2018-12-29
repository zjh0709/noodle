import argparse
from command.spider import reset_article, reset_topic, run_article, run_topic


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--job", dest="job", default=None)
    parser.add_argument("--sub", dest="sub", default=None)
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
