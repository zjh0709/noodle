import argparse
from noodle.job import scrapy

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--job", dest="job", default=None)
    parser.add_argument("--sub", dest="sub", default=None)
    args = parser.parse_args()
    if args.job == "scrapy" and args.sub == "reset_topic":
        scrapy.reset_topic()
    elif args.job == "scrapy" and args.sub == "topic":
        scrapy.run_topic()
    elif args.job == "scrapy" and args.sub == "topic_all":
        scrapy.run_topic(mode="all")
    elif args.job == "scrapy" and args.sub == "reset_article":
        scrapy.reset_article()
    elif args.job == "scrapy" and args.sub == "article":
        scrapy.run_article()
