from db_manager import EntityDatabaseManager
from utils import response


db = EntityDatabaseManager()


def handler(event, context):
    params = event.get("pathParameters", dict()) or dict()  # event can have it as None
    username = params.get("username", None)
    if not username:
        all_entities = db.get_all()
        return response(200, all_entities)

    entity = db.get_entity(username)
    if not entity:
        return response(404, {"message": "No such entity."})

    return response(200, {username: entity})
