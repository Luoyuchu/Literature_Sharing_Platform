from modules import db, auth
from datetime import datetime
from modules.utils import get_json_value, bson_parse, id_parse
from flask import current_app, jsonify, Blueprint, request
from pymongo import ReturnDocument

bp = Blueprint('note', __name__, url_prefix="/note")

reponse_message = {
    "invalid_operate": {
        "message": "Invalid operation.",
        "succeed": False
    },
    "existing_note": {
        "message": "There is existed note for this paper.",
        "succeed": False
    },
    "update_succeed": {
        "message": "Update succeed.",
        "succeed": True
    }
}


def notedb():
    return getattr(db.get_db(), current_app.config['MONGO_NOTE_COLLECTION'])


@bp.route("/create", methods=["POST"])
@auth.login_required
def create_note(user):
    user_id, paper_id, r = get_json_value(
        request.get_json(), 'user_id', "paper_id")
    if not r or str(user['_id']) != user_id:
        return jsonify(reponse_message['invalid_operate']), 401
    r = notedb().find_one({"user_id": user_id, "paper_id": paper_id})
    if r is not None:
        return jsonify(reponse_message['existing_note']), 401
    r = notedb().insert_one({"username": user['username'], "user_id": user_id, "paper_id": paper_id, "public": True,
                             "content": "", "time": datetime.utcnow().replace(microsecond=0)})
    return jsonify(bson_parse(notedb().find_one({"_id": id_parse(r.inserted_id)}))), 201


@ bp.route("/update", methods=["POST"])
@ auth.login_required
def update_note(user):
    query_parameters = request.args
    delete = str(query_parameters.get("delete")) == "true"
    _id, content, public, r = get_json_value(
        request.get_json(), '_id', 'content', "public")
    note = notedb().find_one({"_id": id_parse(_id)})
    if not r or note is None or str(user['_id']) != note['user_id']:
        return jsonify(reponse_message['invalid_operate']), 401

    if delete:
        notedb().find_one_and_delete({"_id": id_parse(_id)})
    else:
        notedb().find_one_and_update({"_id": id_parse(_id)}, {"$set": {
            "content": content, "public": public, "time": datetime.utcnow().replace(microsecond=0)}})
    return jsonify({"message": reponse_message['update_succeed']}), 201


@ bp.route("/query", methods=["GET"])
@ auth.role_identify
def query_note(user):
    query_parameters = request.args
    paper_id = query_parameters.get("paper_id")
    user_id = query_parameters.get("user_id")

    q = {}
    if paper_id is not None:
        q["paper_id"] = paper_id
    if user_id is not None:
        q["user_id"] = user_id
    if user is None:
        q["public"] = True
    else:
        q["$or"] = [{"public": True}, {"user_id": str(user['_id'])}]
    return jsonify(bson_parse(notedb().find(q))), 200
