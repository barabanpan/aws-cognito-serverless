import json


def response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }


entities = {
    "first": "Name: Lily, description: pretty",
    "second": "Name: Vita, description: wise",
    "third": "Name: Debby, description: fluffy"
}


def handler(event, context):
    params = event.get("pathParameters", dict()) or dict()  # event can have it as None
    uid = params.get('id', None)
    if not uid:
        return response(200, entities)

    entity = entities.get(uid, None)
    if not entity:
        return response(404, {"message": "No such entity."})

    return response(200, {uid: entity})
