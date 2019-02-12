import traceback
from operator import itemgetter

from flask import Blueprint, session, g, jsonify
from pymongo.database import Database

from conn.client import mongodb_client

module = Blueprint(name='stat_index', import_name=__name__)


@module.before_request
def before():
    g.db: Database = mongodb_client()
    g.db.get_collection("finance") \
        .find({"category": "summary", "name": "商誉"},
              {"code": 1, "name": 1, "value": 1})


@module.route("/boom/goodwill")
def boom_goodwill():
    captial = g.db.get_collection("finance") \
        .find({"category": "balance", "name": "资产总计"},
              {"_id": 0, "code": 1, "name": 1, "value": 1})
    captial = {d["code"]: d["value"] for d in captial}
    goodwill = g.db.get_collection("finance") \
        .find({"category": "balance", "name": "商誉"},
              {"_id": 0, "code": 1, "name": 1, "value": 1})
    goodwill = {d["code"]: d["value"] for d in goodwill}
    boom = []
    for code in captial.keys():
        # noinspection PyBroadException
        try:
            cp = float(captial[code])
            gw = float(goodwill[code])
            boom.append((code, gw / cp))
        except Exception:
            boom.append((code, -1))
    boom = sorted(boom, key=itemgetter(1), reverse=True)
    return jsonify(boom)


if __name__ == '__main__':
    db = mongodb_client()
    cur = db.get_collection("finance") \
        .find({"category": "balance", "name": "资产总计"},
              {"_id": 0, "code": 1, "name": 1, "value": 1})
    print(next(cur))
