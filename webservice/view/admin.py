from flask import Blueprint, session, g, jsonify, render_template


module = Blueprint(name='admin_view', import_name=__name__)


@module.route("/words")
def words():
    return render_template("admin_words.html")
