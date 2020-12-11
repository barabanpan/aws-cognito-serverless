import boto3
from botocore.exceptions import ClientError, ParamValidationError
import json
import os
import re

from constants import COGNITO_USER_POOL_GROUPS
from db_manager import UsersDatabaseManager
from utils import bad_request, response


client = boto3.client("cognito-idp")
CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID")
USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID")


# TODO: add marshmallow validation of input
def handler(event, context):
    body = json.loads(event["body"])  # TODO: catch json decode error here
    username, password, group = body.get("email"), body.get("password"), body.get("group")

    if not (username and password and group):
        return bad_request("'email', 'password' or 'group' is missing")
    if group not in COGNITO_USER_POOL_GROUPS:
        return bad_request("Choose 'group' from: {0}".format(str(COGNITO_USER_POOL_GROUPS)))

    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", username):
        return bad_request("Invalid email address")

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

    client.admin_add_user_to_group(
        UserPoolId=USER_POOL_ID,
        Username=username,
        GroupName=group
    )

    db = UsersDatabaseManager(username)
    db.add_new_user()

    return response(200, {"message": "Please check your email for verification link."})
