from bson.json_util import dumps
from json import loads
from bson.objectid import ObjectId


def bson_parse(data):
    # print(loads(dumps(data)))
    return loads(dumps(data, ensure_ascii=False))


def id_parse(id):
    return ObjectId(id)


def get_json_value(data, *args):
    r = []
    flag = True
    for i in args:
        if data is None or (i not in data):
            r.append(None)
            flag = False
        else:
            r.append(data[i])
    r.append(flag)
    return r
