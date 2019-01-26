from conn import util
from spider.websites import sina, jrj, wangyi, eastmoney, hexun
from runner.SpiderRunner import SpiderRunner
import logging


def get_stock_len() -> int:
    return SpiderRunner().get_stock_len()


def get_topic_len() -> int:
    return SpiderRunner().get_topic_len()


def get_jobs() -> list():
    return util.get_jobs_all()


@util.register_job()
def reset_stock():
    if len(util.get_jobs("reset_stock")) > 1:
        logging.warning("job reset_stock exists!")
    else:
        SpiderRunner().reset_stock()


@util.register_job()
def reset_topic():
    if len(util.get_jobs("reset_topic")) > 1:
        logging.warning("job reset_topic exists!")
    else:
        SpiderRunner().reset_topic()


@util.register_job()
def run_sina_report_topic():
    SpiderRunner().topic_runner(sina.SinaReport())


@util.register_job()
def run_sina_report_topic_all():
    SpiderRunner().topic_runner_all(sina.SinaReport())


@util.register_job()
def run_sina_report_article():
    SpiderRunner().article_runner(sina.SinaReport())


@util.register_job()
def run_jrj_report_topic():
    SpiderRunner().topic_runner(jrj.JrjReport())


@util.register_job()
def run_jrj_report_topic_all():
    SpiderRunner().topic_runner_all(jrj.JrjReport())


@util.register_job()
def run_jrj_report_article():
    SpiderRunner().article_runner(jrj.JrjReport())


@util.register_job()
def run_jrj_news_topic():
    SpiderRunner().topic_runner(jrj.JrjNews())


@util.register_job()
def run_jrj_news_topic_all():
    SpiderRunner().topic_runner_all(jrj.JrjNews())


@util.register_job()
def run_jrj_news_article():
    SpiderRunner().article_runner(jrj.JrjNews())


@util.register_job()
def run_eastmoney_report_topic():
    SpiderRunner().topic_runner(eastmoney.EastmoneyReport())


@util.register_job()
def run_eastmoney_report_topic_all():
    SpiderRunner().topic_runner_all(eastmoney.EastmoneyReport())


@util.register_job()
def run_eastmoney_report_article():
    SpiderRunner().article_runner(eastmoney.EastmoneyReport())


@util.register_job()
def run_wangyi_report_topic():
    SpiderRunner().topic_runner(wangyi.WangyiReport())


@util.register_job()
def run_wangyi_report_topic_all():
    SpiderRunner().topic_runner_all(wangyi.WangyiReport())


@util.register_job()
def run_wangyi_report_article():
    SpiderRunner().article_runner(wangyi.WangyiReport())
