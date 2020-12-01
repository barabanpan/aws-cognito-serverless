from db_manager import EntityDatabaseManager
from utils import response


db = EntityDatabaseManager()


def handler(event, context):
    params = event.get("pathParameters", dict()) or dict()  # event can have it as None
    uid = params.get("uid", None)
    if not uid:
        all_entities = db.get_all()
        return response(200, all_entities)

    entity = db.get_entity(uid)
    if not entity:
        return response(404, {"message": "No such entity."})

    return response(200, {uid: entity})
