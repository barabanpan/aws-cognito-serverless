import boto3
from botocore.exceptions import ClientError
import os

from basic_auth import decode, DecodeError
from utils import unauthorized, response


client = boto3.client("cognito-idp")
CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID")


def handler(event, context):
    try:
        username, password = decode(event["headers"]["Authorization"])
        username = username.lower()
        res = client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            ClientId=CLIENT_ID,
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password
            }
        )
    except (DecodeError, ClientError):
        return unauthorized()

    res = {
        "AccessToken": res["AuthenticationResult"]["AccessToken"],
        "ExpiresIn": res["AuthenticationResult"]["ExpiresIn"],
        "RefreshToken": res["AuthenticationResult"]["RefreshToken"],
        "TokenType": res["AuthenticationResult"]["TokenType"]
    }
    return response(200, res)
