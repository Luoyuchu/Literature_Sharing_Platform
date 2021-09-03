import os
from flask import Blueprint, request, send_file, current_app, jsonify
from modules import auth, db
from modules.utils import bson_parse, id_parse, get_json_value

bp = Blueprint("annotation", __name__,
               url_prefix="/annotation")


def annotationdb():
    return getattr(db.get_db(), current_app.config['MONGO_ANNOTATION_COLLECTION'])


@bp.route("/query", methods=["GET"])
def annotation_query():
    query_parameters = request.args
    paper_id = query_parameters.get("paper_id")
    if paper_id == None:
        return "invalid parameters", 400
    return jsonify(bson_parse(annotationdb().find({"paper_id": paper_id}))), 200


@bp.route("/update", methods=["POST"])
@auth.login_required
def annotation_update(user):
    added_list, updated_list, deleted_list, r = get_json_value(
        request.get_json(), "added", "updated", "deleted")
    # print("annotation/update", added_list, updated_list, deleted_list, r, user)
    if not r:
        return "invalid parameters", 400
    for i in added_list + updated_list + deleted_list:
        # print("annotation/update", i['user_id'], str(user["_id"]))
        if not (i['user_id'] == str(user["_id"])):
            return "unauthorized annotation operation", 401
    for i in added_list + updated_list:
        annotationdb().find_one_and_update({"uid": i['uid']}, {"$set": {"user_id": i['user_id'], "paper_id": i['paper_id'],
                                                                        'content': i['content']}}, upsert=True)
    for i in deleted_list:
        annotationdb().find_one_and_delete({"uid": i['uid']})
    return "succeed", 200
