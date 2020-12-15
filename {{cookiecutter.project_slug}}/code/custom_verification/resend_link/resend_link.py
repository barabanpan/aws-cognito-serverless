import boto3
import json
import os

from utils import bad_request, BadRequestException, response


COGNITO_CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID")
COGNITO_USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID")
client = boto3.client("cognito-idp")


def handler(event, context):
    try:
        email = validate_body(event.get("body"))
    except BadRequestException as e:
        return bad_request(str(e))

    # check if email is in cognito user pool
    try:
        user = client.admin_get_user(
            UserPoolId=COGNITO_USER_POOL_ID,
            Username=email
        )
    except client.exceptions.UserNotFoundException:
        return bad_request("An account with this email was not found.")

    # check if email is verified
    email_verified = [attr["Value"] for attr in user["UserAttributes"] if attr["Name"] == "email_verified"][0]
    if email_verified == "true":
        return bad_request("The account's email is already verified.")

    client.resend_confirmation_code(
        ClientId=COGNITO_CLIENT_ID,
        Username=email
    )

    return response(200, {"message": "Please check your email for verification link."})


def validate_body(body):
    if not body:
        raise BadRequestException("Missing request body")

    try:
        body = json.loads(body)
    except json.decoder.JSONDecodeError:
        raise BadRequestException("Invalid request body")

    if not isinstance(body, dict):
        raise BadRequestException("Invalid request body")

    email = body.get("email")

    if not email:
        raise BadRequestException("'email' is missing")

    return email
