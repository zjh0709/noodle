from flask import Blueprint, g, jsonify
from runner.ModelRunner import ModelRunner

module = Blueprint(name='manager',
                   import_name=__name__)


@module.before_request
def before():
    if not hasattr(g, 'model_runner'):
        g.model_runner = ModelRunner()


@module.route("/words/useful/<page>", methods=["GET"])
def get_useful_words(page: int):
    words = g.model_runner.get_useful_words(int(page))
    return jsonify(words)


@module.route("/words/useless/<page>", methods=["GET"])
def get_useless_word(page: int):
    words = g.model_runner.get_useless_words(int(page))
    return jsonify(words)


@module.route("/words/useless/<word>", methods=["PUT"])
def add_useless_word(word: str):
    result = g.model_runner.add_useless_word(word)
    return jsonify({"count": result})


@module.route("/words/useless/<word>", methods=["DELETE"])
def remove_useless_word(word: str):
    result = g.model_runner.remove_useless_word(word)
    return jsonify({"count": result})
