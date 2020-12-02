from marshmallow import ValidationError

from db_manager import EntityDatabaseManager
from schemas import EntitySchema
from utils import response


db = EntityDatabaseManager()


def handler(event, context):
    """Return items list or one item of uid is set in params."""
    params = event.get("pathParameters") or dict()
    uid = params.get("uid")

    if not uid:
        entities = db.all()
        try:
            entities = EntitySchema().dump(entities, many=True)
        except ValidationError as err:
            return response(400, err.messages)
        except Exception as e:
            return response(400, repr(e))
        return response(200, entities)

    entity = db.get_one(uid)

    if not entity:
        return response(404, {"message": "No such entity."})

    try:
        entity = EntitySchema().dump(entity)
    except ValidationError as err:
        return response(400, err.messages)

    return response(200, entity)
