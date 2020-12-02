
import boto3
import os
import logging

from utils import bad_request, response


client = boto3.client("cognito-idp")
CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID")


def handler(event, context):
    res = {}
    try:
        # to get rid of "Bearer"
        refresh_token = event["headers"]["Authorization"].split()[1]
        res = client.initiate_auth(
            AuthFlow="REFRESH_TOKEN",
            ClientId=CLIENT_ID,
            AuthParameters={"REFRESH_TOKEN": refresh_token}
        )
    except client.exceptions.NotAuthorizedException:
        err_msg = "Invalid Refresh Token"
        logging.warning(f"!!! NotAuthorizedException: {err_msg}")
        return bad_request(err_msg)
    except Exception as e:
        logging.warning(f"!!! Other Exception: {e}")
        return bad_request(repr(e))
    res = {
        "AccessToken": res["AuthenticationResult"]["AccessToken"],
        "ExpiresIn": res["AuthenticationResult"]["ExpiresIn"],
        "TokenType": res["AuthenticationResult"]["TokenType"]
    }
    return response(200, res)
