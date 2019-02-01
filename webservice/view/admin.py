from flask import Blueprint, session, g, jsonify, render_template


module = Blueprint(name='admin_view', import_name=__name__)


@module.route("/")
def admin():
    return render_template("admin.html")
