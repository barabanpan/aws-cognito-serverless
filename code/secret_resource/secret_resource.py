import json


def handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hi! That's a secret resource! The answer is 42."})
    }
