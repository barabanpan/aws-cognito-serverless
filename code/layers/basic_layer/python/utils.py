import json
from marshmallow import Schema, fields, validate

from constants import DEFAULT_IS_GOOD_BOY, DATE_FORMAT


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


# schema for marshmallow validation
class EntitySchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=30))
    email = fields.Email(required=True)
    description = fields.String(required=True, validate=validate.Length(min=1, max=500))
    value = fields.Integer(required=True, validate=validate.Range(min=1, max=1000))
    date = fields.Date(required=True, format=DATE_FORMAT)
    is_good_boy = fields.Boolean(required=False, default=DEFAULT_IS_GOOD_BOY)
