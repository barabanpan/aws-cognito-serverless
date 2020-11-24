import boto3
import os

from basic_auth import decode  # , DecodeError
from utils import bad_request, response


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
    except Exception as e:
        print("-----------EXCEPTION:", e)
        return bad_request(str(e))

# Common exceptions:
# (UserNotFoundException) when calling the InitiateAuth operation: User does not exist
#
# DecodeError
# (InvalidParameterException) when calling the InitiateAuth operation: Missing required parameter PASSWORD / USERNAME
# KeyError
# All mean mallformed something:)
#
# (UserNotConfirmedException) when calling the InitiateAuth operation: User is not confirmed
    else:
        res = {
            "AccessToken": res["AuthenticationResult"]["AccessToken"],
            "ExpiresIn": res["AuthenticationResult"]["ExpiresIn"],
            # "IdToken": res["AuthenticationResult"]["IdToken"],
            # if we need IdToken, we can just do res = res["AuthenticationResult"]
            "RefreshToken": res["AuthenticationResult"]["RefreshToken"],
            "TokenType": res["AuthenticationResult"]["TokenType"]
        }
    return response(200, res)
