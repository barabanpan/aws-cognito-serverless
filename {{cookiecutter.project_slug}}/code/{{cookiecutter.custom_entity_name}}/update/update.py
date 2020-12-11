import json

from marshmallow import ValidationError

from db_manager import EntityDatabaseManager
from decorators import verify_JWT_token
from schemas import EntitySchema
from utils import bad_request, response


db = EntityDatabaseManager()


@verify_JWT_token(group="modifier")
def handler(event, context):
    """Update existed custom entity."""

    entity = None
    params = event.get("pathParameters", dict()) or dict()
    uid = params.get("uid", None)

    try:
        entity = json.loads(event.get("body"))
    except json.decoder.JSONDecodeError as e:
        return bad_request("Invalid request body: {0}".format(str(e)))

    try:
        entity = EntitySchema().load(entity)
    except ValidationError as err:
        return response(400, err.messages)

    if entity and uid:
        entity, ok = db.create_or_update(item=entity, uid=uid)
        if ok:
            # If entity updated successfylly then return it in responce
            try:
                entity = EntitySchema().dump(entity)
            except ValidationError as err:
                return response(400, err.messages)

            entity.update({"success": True})

            return response(200, entity)

    return response(404, {"status": "Not Found"})
