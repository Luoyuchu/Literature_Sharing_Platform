from json import dumps
from modules import auth, db, paper
from modules.utils import get_json_value
from flask import current_app, Blueprint, request, jsonify

bp = Blueprint('rating', __name__, url_prefix="/rating")


def ratingdb():
    return getattr(db.get_db(), current_app.config['MONGO_RATING_COLLECTION'])


reponse_message = {
    "invalid_operate": {
        "message": "Invalid operation.",
        "succeed": False
    },
    "update_succeed": {
        "message": "Update succeed.",
        "succeed": True
    }
}


@bp.route("/query", methods=["GET"])
def query_rating():
    query_parameters = request.args
    paper_id = query_parameters.get("paper_id")
    user_id = query_parameters.get("user_id")

    if paper_id is None:
        return jsonify(reponse_message['invalid_operate']), 401
    q = {"paper_id": paper_id}
    if user_id is not None:
        q["user_id"] = user_id
    r = ratingdb().aggregate(
        [{"$match": q}, {"$group": {"_id": None, "rating": {"$avg": "$rating"}, "num_rating": {"$sum": 1}}}])
    r = list(r)
    if len(r) > 0:
        return jsonify({**r[0], "succeed": True, "norecord": False}), 200
    else:
        return jsonify({"succeed": True, "norecord": True}), 200


@bp.route("/update", methods=["POST"])
@auth.login_required
def update_rating(user):
    paper_id, user_id, rating, r = get_json_value(
        request.get_json(), "paper_id", "user_id", "rating")
    if not r or str(user['_id']) != user_id:
        return jsonify(reponse_message['invalid_operate']), 401
    ratingdb().find_one_and_update({"paper_id": paper_id, "user_id": user_id}, {
        "$set": {"rating": rating}}, upsert=True)
    r = ratingdb().aggregate(
        [{"$match": {"paper_id": paper_id}}, {"$group": {"_id": None, "rating": {"$avg": "$rating"}, "num_rating": {"$sum": 1}}}])
    return jsonify({**(list(r)[0]), "succeed": True}), 201
