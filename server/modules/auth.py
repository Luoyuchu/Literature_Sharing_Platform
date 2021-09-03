import jwt
from modules import db
from functools import wraps
from datetime import datetime
from modules.utils import get_json_value, bson_parse
from flask import current_app, jsonify, request, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')
reponse_message = {
    "invalid_token": {
        'message': 'Invalid token. Registeration and / or authentication required.',
        'authenticated': False
    },
    "expired": {
        'message': 'Expired token. Reauthentication required',
        'authenticated': False
    },
    "invalid_account": {
        'message': "Invalid email/password/username",
        "succeed": False,
    },
    "existing_email": {
        'message': "Existing email.",
        "succeed": False,
    },
    'signup_succeed': {
        'message': "Sign up succeed.",
        'succeed': True
    },
    "change_password_succeed": {
        "message": "Change password succeed.",
        "succeed": True,
    }
}


def authdb():
    return getattr(db.get_db(), current_app.config['MONGO_AUTH_COLLECTION'])


def get_user(email):
    return authdb().find_one({"email": email})


def check_email(email):
    return not (get_user(email) is None)


def check_passwd(email, passwd):
    return check_email(email) and check_password_hash(get_user(email)['passwd'], passwd)


def get_token(email, passwd):
    if check_passwd(email, passwd):
        user = get_user(email)
        if user is not None and check_passwd:
            token = jwt.encode({
                'email': email,
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + current_app.config['EXPIRE_DURATION']
            }, current_app.config["SECRET_KEY"])
            return token


def login_required(f):
    @wraps(f)
    def wrapped_f(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        if len(auth_headers) != 2:
            return jsonify(reponse_message['invalid_token']), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(
                token, key=current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user = get_user(data['email'])
            if user is None:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            # 401 is Unauthorized HTTP status code
            return jsonify(reponse_message['expired']), 401
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(reponse_message['invalid_token']), 401
    return wrapped_f


def role_identify(f):
    @wraps(f)
    def wrapped_f(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        if len(auth_headers) != 2:
            user = None
        try:
            token = auth_headers[1]
            data = jwt.decode(
                token, key=current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user = get_user(data['email'])
        except:
            user = None
        return f(user, *args, **kwargs)
    return wrapped_f


@bp.route('/login', methods=['POST'])
def login():
    email, passwd, r = get_json_value(request.get_json(), 'email', 'passwd')
    if not r:
        return jsonify(reponse_message['invalid_account']), 401
    token = get_token(email, passwd)
    if token is None:
        return jsonify(reponse_message['invalid_account']), 401
    user = get_user(email)
    return jsonify({'token': token, 'user': bson_parse(user), 'succeed': True}), 200


@ bp.route('signup', methods=['POST'])
def signup():
    email, passwd, username, r = get_json_value(
        request.get_json(), 'email', 'passwd', 'username')
    if not r:
        return jsonify(reponse_message['invalid_account']), 401
    if check_email(email):
        return jsonify(reponse_message['existing_email']), 401
    passwdhash = generate_password_hash(passwd, method='sha256')
    authdb().insert_one(
        {"email": email, "passwd": passwdhash, "username": username})
    return jsonify(reponse_message['signup_succeed']), 201


@ bp.route("changepasswd", methods=['POST'])
@ login_required
def changepasswd(user):
    email, odpd, nwpd, r = get_json_value(
        request.get_json(), 'email', 'old_passwd', 'new_passwd')
    if (not r) or user['email'] != email:
        return jsonify(reponse_message['invalid_account']), 401
    if not check_passwd(email, odpd):
        return jsonify(reponse_message['invalid_account']), 401
    passwdhash = generate_password_hash(nwpd, method='sha256')
    authdb().find_one_and_update(
        {'email': email}, {"$set": {"passwd": passwdhash}})
    return jsonify(reponse_message['change_password_succeed']), 200


# @bp.route('/userprofile', methods=["GET"])
# @login_required
# def userprofile():
#     return jsonify({"message": "succeed!"}), 200
