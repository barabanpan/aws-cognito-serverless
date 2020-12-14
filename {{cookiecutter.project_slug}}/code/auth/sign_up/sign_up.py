import boto3
from botocore.exceptions import ClientError, ParamValidationError
import json
import os
import re

from constants import COGNITO_USER_POOL_GROUPS
from db_manager import UsersDatabaseManager
from utils import bad_request, BadRequestException, response


client = boto3.client("cognito-idp")
CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID")
USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID")


def handler(event, context):
    try:
        username, password, groups = validate_body(event.get("body"))
    except BadRequestException as e:
        return bad_request(str(e))

    try:
        client.sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            Password=password
        )
    except ClientError as error:
        return bad_request(error.response["Error"]["Message"])
    except ParamValidationError as error:
        return bad_request(str(error.kwargs["report"]))

    for group in groups:
        client.admin_add_user_to_group(
            UserPoolId=USER_POOL_ID,
            Username=username,
            GroupName=group
        )

    db = UsersDatabaseManager(username)
    db.add_new_user()

    return response(200, {"message": "Please check your email for verification link."})


def validate_body(body):
    if not body:
        raise BadRequestException("Missing request body")

    try:
        body = json.loads(body)
    except json.decoder.JSONDecodeError as e:
        raise BadRequestException("Invalid request body")

    if not isinstance(body, dict):
        raise BadRequestException("Invalid request body")

    username, password, groups = body.get("email"), body.get("password"), body.get("groups")

    if not (username and password and groups):
        raise BadRequestException("'email', 'password' or 'groups' is missing")

    if not isinstance(groups, list):
        raise BadRequestException("'groups' should be a list")

    for group in groups:
        if group not in COGNITO_USER_POOL_GROUPS:
            raise BadRequestException("Choose 'groups' from: {0}".format(str(COGNITO_USER_POOL_GROUPS)))

    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", username):
        raise BadRequestException("Invalid email address")

    return username, password, groups
