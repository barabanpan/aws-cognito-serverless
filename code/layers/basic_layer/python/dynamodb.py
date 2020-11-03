import boto3
import time
import uuid

TABLE_NAME = "test"


class DatabaseManager:
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(TABLE_NAME)

    def add_new_log(self, request_body, res):
        self.table.put_item(
            Item={
                'uid': str(uuid.uuid4()),
                'timestamp': int(time.time()),
                'request_body': request_body,
                'res': res
            }
        )
