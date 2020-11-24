import json


def response(code, body):
    return {"statusCode": code,
            "headers": {
                "X-Requested-With": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps(body)}


def bad_request(message):
    return response(400, {"message": message})


class Entity:
    def __init__(self, username, email, description, value, date, is_good_boy):
        self.username = username
        self.email = email
        self.description = description
        self.value = value
        self.date = date
        self.is_good_boy = is_good_boy
