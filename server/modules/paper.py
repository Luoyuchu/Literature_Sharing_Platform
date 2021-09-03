import os
from flask import Blueprint, request, send_file, current_app, jsonify
from modules import auth, db
from modules.utils import bson_parse, id_parse

bp = Blueprint("paper", __name__, url_prefix="/paper")


def paperdb():
    return getattr(db.get_db(), current_app.config['MONGO_PAPER_COLLECTION'])


@bp.route('/resources/paper', methods=['GET'])
def get_paper():
    query_parameters = request.args
    filename = query_parameters.get("filename")
    return send_file(current_app.config['PAPER_PATH'] + os.sep + filename + ".pdf")


@bp.route('/paperlist', methods=['GET'])
def get_paperlist():
    return jsonify(bson_parse(db.get_db().paper.find({"file_ready": True}))), 200


@bp.route('/paperinfo', methods=["GET"])
def query_paper():
    query_parameters = request.args
    filename = query_parameters.get("filename")
    id = query_parameters.get("paperid")
    q = {}
    if filename is not None:
        q['filename'] = filename
    if id is not None:
        q['_id'] = id_parse(id)
    return jsonify(bson_parse(paperdb().find_one(q))), 200
