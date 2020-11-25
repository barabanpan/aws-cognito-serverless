from utils import response


def handler(event, context):
    return response(200, {"message": "Hi! That's a secret resource! The answer is 42."})
