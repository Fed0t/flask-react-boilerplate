import json
from bson import ObjectId


def check_payload(data, keys):
    for key in keys:
        if key not in data:
            return False
    return True

# def check_transaction(self, keys):
#     for key in keys:
#         if key not in data:
#             return False
#     return True


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)