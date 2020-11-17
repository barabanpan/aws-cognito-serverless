import boto3
import time
import os


USERS_TABLE_NAME = os.environ.get('USERS_TABLE_NAME')


class DatabaseManager:
    def __init__(self, customer_email):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(USERS_TABLE_NAME)
        self.customer_email = customer_email

    def write_new_user_info(self):
        self.table.put_item(
            Item={
                'email': self.customer_email,
                'sign_up_date': int(time.time())
            }
        )
