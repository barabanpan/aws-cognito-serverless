import boto3
import os

cognito = boto3.client("cognito-idp")
CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID")
REDIRECT_URL = os.environ.get("URL_FOR_REDIRECT_AFTER_COGNITO_VERIFICATION")


def lambda_handler(event, context):
    params = event.get("queryStringParameters") or dict()  # can be None in event
    email, code = params.get("email"), params.get("code")

    cognito.confirm_sign_up(
        ClientId=CLIENT_ID,
        Username=email,
        ConfirmationCode=code,
    )

    return {
        "statusCode": 302,
        "headers": {"Location": REDIRECT_URL}
    }
