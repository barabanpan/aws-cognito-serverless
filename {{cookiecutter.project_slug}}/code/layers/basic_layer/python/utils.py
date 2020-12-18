import json


def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "X-Requested-With": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Credentials": "true"
        },
        "body": json.dumps(body)
    }


def bad_request(message):
    return response(400, {"message": message})


def unauthorized():
    return response(401, {"message": "Unauthorized"})


class BadRequestException(Exception):
    pass


def redirect_to(redirect_url):
    return {
        "statusCode": 302,
        "headers": {
            "Location": redirect_url,
            "X-Requested-With": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Credentials": "true"
        }
    }
