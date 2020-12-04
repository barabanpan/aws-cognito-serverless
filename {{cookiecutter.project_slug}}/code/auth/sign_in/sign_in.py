import boto3
from botocore.exceptions import ClientError
import os
import logging

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
    except (DecodeError, ClientError) as err:
        logging.warning(repr(err))
        return unauthorized()
 
    auth_result = res.get("AuthenticationResult", {})
    res = {
        "AccessToken": auth_result.get("AccessToken", ""),
        "ExpiresIn": auth_result.get("ExpiresIn", ""),
        "RefreshToken": auth_result.get("RefreshToken", ""),
        "TokenType": auth_result.get("TokenType", ""),
    }
    return response(200, res)
