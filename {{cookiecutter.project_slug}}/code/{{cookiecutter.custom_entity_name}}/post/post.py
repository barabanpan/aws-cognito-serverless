import json

from marshmallow import ValidationError

from db_manager import EntityDatabaseManager
from schemas import EntitySchema
from utils import bad_request, response


db = EntityDatabaseManager()


def handler(event, context):
    """Create new custom entity."""

    new_entity = None

    try:
        new_entity = json.loads(event.get("body"))
    except json.decoder.JSONDecodeError as e:
        return bad_request("Invalid request body: {0}".format(str(e)))

    try:
        new_entity = EntitySchema().load(new_entity)
    except ValidationError as err:
        return response(400, err.messages)

    if new_entity:
        entity = db.create_or_update(item=new_entity)
        return response(201, entity)

    return bad_request("Something went wrong")
