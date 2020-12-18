import boto3
import logging
import os

from utils import redirect_to


cognito = boto3.client("cognito-idp")
CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID")
USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID")
REDIRECT_AFTER_VERIFICATION = os.environ.get("URL_FOR_REDIRECT_AFTER_COGNITO_VERIFICATION")
REDIRECT_WHEN_CODE_EXPIRED = os.environ.get("URL_FOR_REDIRECT_IF_CODE_IS_EXIPIRED")
REDIRECT_WHEN_ALREADY_CONFIRMED = os.environ.get("URL_FOR_REDIRECT_IF_ALREADY_VERIFIED")


def handler(event, context):
    params = event.get("queryStringParameters") or dict()  # can be None in event
    email, code = params.get("email"), params.get("code")

    try:
        cognito.confirm_sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            ConfirmationCode=code,
        )
    except cognito.exceptions.ExpiredCodeException:
        user = cognito.admin_get_user(
            UserPoolId=USER_POOL_ID,
            Username=email
        )

        # check if email is already verified
        email_verified = [attr["Value"] for attr in user["UserAttributes"] if attr["Name"] == "email_verified"][0]
        if email_verified == "true":
            redirect_to(REDIRECT_WHEN_ALREADY_CONFIRMED)

        return redirect_to(REDIRECT_WHEN_CODE_EXPIRED)

    except (cognito.exceptions.CodeMismatchException, cognito.exceptions.LimitExceededException) as e:
        # here should be some page with "Oops, something went wrong. Please request another verification link later"
        logging.warning(repr(e))
        return redirect_to(REDIRECT_WHEN_CODE_EXPIRED)

    return redirect_to(REDIRECT_AFTER_VERIFICATION)
