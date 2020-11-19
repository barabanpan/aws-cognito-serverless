import boto3
import os

from utils import bad_request, response


client = boto3.client('cognito-idp')
CLIENT_ID = os.environ.get('COGNITO_CLIENT_ID')


def handler(event, context):
    try:
        refresh_token = event['headers']['Authorization'].split()[1]  # to get rid of 'Bearer'
        res = client.initiate_auth(
            AuthFlow='REFRESH_TOKEN',
            ClientId=CLIENT_ID,
            AuthParameters={
                'REFRESH_TOKEN': refresh_token
            }
        )
    except Exception as e:
        print('-----------EXCEPTION:', e)
        return bad_request(str(e))

        # Common exceptions:
        # (NotAuthorizedException) when calling the InitiateAuth operation: Invalid Refresh Token
        #
        # KeyError
        #
    else:
        res = {
            'AccessToken': res['AuthenticationResult']['AccessToken'],
            'ExpiresIn': res['AuthenticationResult']['ExpiresIn'],
            # 'IdToken': res['AuthenticationResult']['IdToken'],
            # якщо це не треба закоментовувати, то можна просто брати весь res['AuthenticationResult']
            'TokenType': res['AuthenticationResult']['TokenType']
        }
        return response(200, res)
