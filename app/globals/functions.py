from bson import json_util
import json


def serialize_mongo_output(docs):
    if docs:
        return json.loads(json_util.dumps(docs))

    return docs
