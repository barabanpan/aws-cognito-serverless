import json

from dynamodb import DatabaseManager


def log_request(func):
    def wrapper(event, context):
        request_body = event['body']
        result = func(event, context)

        # log request
        db = DatabaseManager()
        db.add_new_log(request_body, json.loads(result['body'])['res'])

        return result
    return wrapper
