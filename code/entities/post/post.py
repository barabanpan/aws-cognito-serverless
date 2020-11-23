import json

from db_manager import EntityDatabaseManager
from utils import bad_request, Entity, response


db = EntityDatabaseManager()


def handler(event, context):
    try:
        new_entity = json.loads(event.get("body", dict()))
    except Exception:
        return bad_request("Invalid request body")

    # add a better validation
    try:
        entity = Entity(new_entity['username'], new_entity['email'],
                        new_entity['description'], new_entity['value'],
                        new_entity['date'], new_entity['is_good_boy'])
        db.add_new_entity(entity)

    except Exception as e:
        return bad_request(repr(e))

    return response(201, {"new_entity": new_entity})
