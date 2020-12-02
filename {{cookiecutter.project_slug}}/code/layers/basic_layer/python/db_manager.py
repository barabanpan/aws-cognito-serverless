import time
import os
import uuid
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Attr

from constants import DATETIME_FORMAT


USERS_TABLE_NAME = os.environ.get("USERS_TABLE_NAME")
ENTITY_TABLE_NAME = os.environ.get("CUSTOM_ENTITY_TABLE_NAME")


class UsersDatabaseManager:
    def __init__(self, customer_email):
        dynamodb = boto3.resource("dynamodb")
        self.table = dynamodb.Table(USERS_TABLE_NAME)
        self.customer_email = customer_email

    def add_new_user(self):
        self.table.put_item(
            Item={
                "email": self.customer_email,
                "sign_up_date": int(time.time())
            }
        )


class EntityDatabaseManager:

    def __init__(self):
        dynamodb = boto3.resource("dynamodb")
        self.table = dynamodb.Table(ENTITY_TABLE_NAME)

    def _create(self, item):
        """Create new db record."""
        created = False
        extra_fields = {
            "uid": str(uuid.uuid4()),
            "created_at": datetime.now().astimezone().strftime(
                DATETIME_FORMAT),
            "updated_at": datetime.now().astimezone().strftime(
                DATETIME_FORMAT),
            "is_active": True,
        }
        if item:
            item.update(extra_fields)
            created = self.table.put_item(Item=item)
            if created:
                item.update({"success": True})
        return item

    def _update(self, uid, item):
        """Update existed item."""
        # TODO
        updated = self.table.update_item(
            Key={'uid': 'uid'},
            UpdateExpression='SET updated_at = :val1',
            ExpressionAttributeValues={
                ':val1': datetime.now().strftime(DATETIME_FORMAT)
            }
        )
        print("!!! updated", updated)
        return updated

    def create_or_update(self, item=None, uid=None):
        if not uid:
            item = self._create(item=item)
        else:
            item = self._update(uid=uid, item=item)
        return item

    def get_one(self, uid):
        entity = self.table.get_item(Key={"uid": uid}).get("Item")
        if not entity:
            return None
        return entity

    def all(self):
        all_entities = self.table.scan()["Items"]
        return list(all_entities)

    def delete_entity(self, uid):
        self.table.delete_item(Key={"uid": uid})

    def find_by_email(self, email):
        """Get all items selected by email field."""
        response = self.table.scan(
            FilterExpression=Attr('email').eq(email)
        )
        items = response['Items']
        return items
