from flask import Blueprint, g, jsonify
from runner.ModelRunner import ModelRunner

module = Blueprint(name='manager',
                   import_name=__name__)


@module.before_request
def before():
    if not hasattr(g, 'model_runner'):
        g.model_runner = ModelRunner()


@module.route("/words")
def get_words():
    g.model_runner.get_words()


