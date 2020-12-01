import json
from marshmallow import ValidationError

from constants import DATE_FORMAT, DEFAULT_IS_GOOD_BOY
from db_manager import EntityDatabaseManager
from utils import bad_request, Entity, EntitySchema, response


db = EntityDatabaseManager()


def handler(event, context):
    try:
        new_entity = json.loads(event.get("body", dict()))
    except Exception:
        return bad_request("Invalid request body")

    # validation
    try:
        new_entity = EntitySchema().load(new_entity)
        # if value is '21', it will be a number in new_entity
    except ValidationError as ve:
        return bad_request(str(ve.messages))

    try:
        entity = Entity(new_entity["username"], new_entity["email"],
                        new_entity["description"], new_entity["value"],
                        new_entity["date"].strftime(DATE_FORMAT),
                        new_entity.get("is_good_boy", DEFAULT_IS_GOOD_BOY))
        db.add_new_entity(entity)
    except Exception as e:
        return bad_request(repr(e))

    return response(201, {"message": "Added successfully."})
