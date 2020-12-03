from db_manager import EntityDatabaseManager
from utils import response


db = EntityDatabaseManager()


def handler(event, context):
    """Delete or deactivate entity."""
    params = event.get("pathParameters", dict()) or dict()
    uid = params.get("uid", None)

    is_deleted = db.delete(uid)

    if is_deleted:
        return response(204, {})

    return response(404, {"status": "Not Found"})
