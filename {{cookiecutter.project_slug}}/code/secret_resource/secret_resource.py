from utils import response


def handler(event, context):
    """Is a private resource. Requires an access token."""
    return response(200, {"message": "Hi! That's a secret resource! The answer is 42."})
