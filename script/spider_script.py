import datetime

from runner.SpiderRunner import SpiderRunner, logger
from spider.websites import sina, jrj, wangyi, eastmoney, hexun


def reset_stock():
    SpiderRunner().reset_stock()


def reset_topic():
    SpiderRunner().reset_topic()


def reset_date():
    SpiderRunner().reset_date()


def clear_stock():
    SpiderRunner().clear_stock()


def clear_topic():
    SpiderRunner().clear_topic()


def clear_date():
    SpiderRunner().clear_date()


def run_topic(mode="append"):
    assert mode in ("append", "overwrite")
    spider_runner = SpiderRunner()
    sina_report = sina.SinaReport()
    jrj_report = jrj.JrjReport()
    jrj_news = jrj.JrjNews()
    wangyi_report = wangyi.WangyiReport()
    eastmoney_report = eastmoney.EastmoneyReport()
    while True:
        code = spider_runner.next_stock()
        if code is None:
            logger.warning("no stock!")
            break
        spider_runner.topic_runner(sina_report, code, mode)
        spider_runner.topic_runner(jrj_report, code, mode)
        spider_runner.topic_runner(jrj_news, code, mode)
        spider_runner.topic_runner(wangyi_report, code, mode)
        spider_runner.topic_runner(eastmoney_report, code, mode)


def run_article():
    spider_runner = SpiderRunner()
    sina_report = sina.SinaReport()
    jrj_report = jrj.JrjReport()
    jrj_news = jrj.JrjNews()
    wangyi_report = wangyi.WangyiReport()
    eastmoney_report = eastmoney.EastmoneyReport()
    while True:
        topic = spider_runner.next_topic()
        if topic is None:
            logger.warning("no topic!")
            break
        spider_runner.article_runner(sina_report, topic)
        spider_runner.article_runner(jrj_report, topic)
        spider_runner.article_runner(jrj_news, topic)
        spider_runner.article_runner(wangyi_report, topic)
        spider_runner.article_runner(eastmoney_report, topic)


def run_info():
    spider_runner = SpiderRunner()
    sina_info = sina.SinaInfo()
    hexun_info = hexun.HexunInfo()
    while True:
        code = spider_runner.next_stock()
        if code is None:
            logger.warning("no stock!")
            break
        spider_runner.info_runner(sina_info, code)
        spider_runner.info_runner(hexun_info, code)


def run_finance():
    spider_runner = SpiderRunner()
    sina_info = sina.SinaInfo()
    while True:
        code = spider_runner.next_stock()
        if code is None:
            logger.warning("no stock!")
            break
        spider_runner.finance_runner(sina_info, code)


def run_offline():
    spider_runner = SpiderRunner()
    while True:
        dt = spider_runner.next_date()
        if dt is None:
            logger.warning("no date!")
            break
        spider_runner.offline_runner(dt)


def run_offline_yesterday():
    spider_runner = SpiderRunner()
    spider_runner.offline_runner()


def run_offline_today():
    today = datetime.datetime.now().strftime("%Y%m%d")
    spider_runner = SpiderRunner()
    spider_runner.offline_runner(today)


def run_online():
    spider_runner = SpiderRunner()
    spider_runner.online_runner()


if __name__ == '__main__':
    run_offline_today()
