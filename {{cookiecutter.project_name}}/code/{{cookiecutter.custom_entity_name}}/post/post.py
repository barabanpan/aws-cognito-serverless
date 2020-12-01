import json
from marshmallow import ValidationError

from constants import DATE_FORMAT, DEFAULT_IS_GOOD_BOY
from db_manager import EntityDatabaseManager
from utils import bad_request, Entity, EntitySchema, response_201


db = EntityDatabaseManager()


def handler(event, context):
    try:
        new_entity = json.loads(event.get("body", dict()))
    except json.decoder.JSONDecodeError as e:
        return bad_request("Invalid request body: {0}".format(str(e)))

    # validation
    try:
        new_entity = EntitySchema().load(new_entity)
        # if value is '21', it will be a number in new_entity
    except ValidationError as ve:
        return bad_request(str(ve.messages))

    entity = Entity(new_entity["username"], new_entity["email"],
                    new_entity["description"], new_entity["value"],
                    new_entity["date"].strftime(DATE_FORMAT),
                    new_entity.get("is_good_boy", DEFAULT_IS_GOOD_BOY))

    # check if entity already exists
    existing_entity = db.get_entity(entity.username)
    if existing_entity:
        return bad_request("Entity with this username already exists!")

    db.add_new_entity(entity)

    return response_201()
