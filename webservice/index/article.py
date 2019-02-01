from flask import Blueprint, session, g, jsonify
from runner.SpiderRunner import SpiderRunner


module = Blueprint(name='article_index', import_name=__name__)


@module.before_request
def before():
    if not hasattr(g, 'spider_runner'):
        g.spider_runner = SpiderRunner()



