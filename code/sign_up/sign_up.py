import boto3
from botocore.exceptions import ClientError, ParamValidationError
import re

from cognito import CLIENT_ID, get_secret_hash
from db_manager import DatabaseManager
from utils import bad_request, response


client = boto3.client('cognito-idp')


# TODO: add validation of json data
def handler(event, context):
    body = event['body']
    username = body['email']
    if not re.fullmatch(r'[^@]+@[^@]+\.[^@]+', username):
        return bad_request('Invalid email address')

    # should be last, is first here for testing purposes only
    db = DatabaseManager(username)
    db.write_new_user_info()

    secret_hash = get_secret_hash(username)
    try:
        client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=secret_hash,
            Username=username,
            Password=body['password']
        )
    except ClientError as error:
        return bad_request(error.response['Error']['Message'])
    except ParamValidationError as error:
        return bad_request(str(error.kwargs['report']))

    return response(200, {'message': 'Please check your email for verification link.'})
