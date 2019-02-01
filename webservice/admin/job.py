from flask import Blueprint, g, jsonify
from runner.SpiderRunner import SpiderRunner


module = Blueprint(name='job_admin',
                   import_name=__name__)


@module.before_request
def before():
    if not hasattr(g, 'spider_runner'):
        g.spider_runner = SpiderRunner()


@module.route("/stockLeft")
def get_stock_left():
    stock_left = g.spider_runner.get_stock_left()
    data = {"stock": stock_left, "count": len(stock_left)}
    return jsonify(data)


@module.route("/topicLeft")
def get_topic_left():
    topic_left = g.spider_runner.get_topic_left()
    data = {"topic": topic_left, "count": len(topic_left)}
    return jsonify(data)



