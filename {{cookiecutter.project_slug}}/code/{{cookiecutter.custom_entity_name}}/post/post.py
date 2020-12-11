import json

from marshmallow import ValidationError

from db_manager import EntityDatabaseManager
from decorators import verify_JWT_token
from schemas import EntitySchema
from utils import bad_request, response


db = EntityDatabaseManager()


@verify_JWT_token(group="modifier")
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
        # Validate if records with current email already exist
        email = new_entity.get("email")
        items = db.find_by_email(email)
        if items:
            err_message = dict(
                email=[f"Record with email '{email}' already exists", ],
            )
            return response(400, err_message)

        entity, ok = db.create_or_update(item=new_entity)

        try:
            entity = EntitySchema().dump(entity)
        except ValidationError as err:
            return response(400, err.messages)

        # If new record created successfully
        if ok:
            entity.update({"success": True})
            return response(201, entity)

    return bad_request("Something went wrong")
