from db_manager import EntityDatabaseManager
from utils import response


db = EntityDatabaseManager()


def handler(event, context):
    params = event.get("pathParameters", dict()) or dict()  # event can have it as None
    uid = params.get("uid", None)

    db.delete_entity(uid)
    return response(200, {"message": "Deleted succesfully."})
