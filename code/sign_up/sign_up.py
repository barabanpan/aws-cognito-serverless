import boto3
from botocore.exceptions import ClientError, ParamValidationError
import json
import os
import re

from db_manager import DatabaseManager
from utils import bad_request, response


client = boto3.client('cognito-idp')
CLIENT_ID = os.environ.get('COGNITO_CLIENT_ID')


# TODO: add validation of json data
def handler(event, context):
    body = json.loads(event['body'])
    username = body['email']
    if not re.fullmatch(r'[^@]+@[^@]+\.[^@]+', username):
        return bad_request('Invalid email address')

    # should be last, is first here for testing purposes only
    db = DatabaseManager(username)
    db.write_new_user_info()

    try:
        client.sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            Password=body['password']
        )
    except ClientError as error:
        return bad_request(error.response['Error']['Message'])
    except ParamValidationError as error:
        return bad_request(str(error.kwargs['report']))

    return response(200, {'message': 'Please check your email for verification link.'})
