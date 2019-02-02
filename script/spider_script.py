from runner.SpiderRunner import SpiderRunner, logger
from spider.websites import sina, jrj, wangyi, eastmoney, hexun


def test():
    print("test!")


def reset_stock():
    SpiderRunner().reset_stock()


def reset_topic():
    SpiderRunner().reset_topic()


def clear_stock():
    SpiderRunner.clear_stock()


def clear_topic():
    SpiderRunner.clear_topic()


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


if __name__ == '__main__':
    run_finance()
