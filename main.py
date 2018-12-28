import argparse
from noodle.job import spider

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--job", dest="job", default=None)
    parser.add_argument("--sub", dest="sub", default=None)
    args = parser.parse_args()
    if args.job == "spider" and args.sub == "reset_topic":
        spider.reset_topic()
    elif args.job == "spider" and args.sub == "topic":
        spider.run_topic()
    elif args.job == "spider" and args.sub == "topic_all":
        spider.run_topic(mode="all")
    elif args.job == "spider" and args.sub == "reset_article":
        spider.reset_article()
    elif args.job == "spider" and args.sub == "article":
        spider.run_article()
