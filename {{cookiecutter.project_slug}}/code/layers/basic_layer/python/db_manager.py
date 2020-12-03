import boto3
import time
import os
import uuid
from datetime import datetime

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
        uid = str(uuid.uuid4())
        extra_fields = {
            "uid": uid,
            "created_at": datetime.now().astimezone().strftime(
                DATETIME_FORMAT),
            "updated_at": datetime.now().astimezone().strftime(
                DATETIME_FORMAT),
            "is_active": True,
        }
        if item:
            item.update(extra_fields)
            created = self.table.put_item(Item=item)
        return item, bool(created)

    def _update(self, uid, item):
        """Update existed item."""
        updated = False
        prev_fields = self.get_one(uid)
        if prev_fields:
            new_fields = dict(item)
            new_fields.update({
                "updated_at": datetime.now().astimezone().strftime(
                    DATETIME_FORMAT
                ),
            })
            prev_fields.update(new_fields)
            updated = self.table.put_item(Item=prev_fields)
            item = self.get_one(uid)
        return item, bool(updated)

    def create_or_update(self, item=None, uid=None):
        """Create new or update existed record."""
        if not uid:
            item, success = self._create(item=item)
        else:
            item, success = self._update(uid=uid, item=item)
        return item, success

    def get_one(self, uid):
        """Retrieve one record from db by uid field."""
        entity = self.table.get_item(Key={"uid": uid}).get("Item")
        if not entity:
            return None
        return entity

    def all(self, active_only=True):
        """Retrieve all records or select only active."""
        if active_only:
            response = self.table.scan(
                FilterExpression=Attr("is_active").eq(True)
            )
            entities = response.get("Items", [])
        else:
            entities = self.table.scan()["Items"]
        return list(entities)

    def delete(self, uid, deactivate_only=True):
        """Delete or deactivate current item."""
        deleted = False
        if deactivate_only:
            item = self.get_one(uid)
            if item:
                expression = "SET updated_at = :val1, is_active = :val2"
                deleted = self.table.update_item(
                    Key={"uid": uid},
                    UpdateExpression=expression,
                    ExpressionAttributeValues={
                        ":val1": datetime.now().astimezone().strftime(
                            DATETIME_FORMAT
                        ),
                        ":val2": False
                    }
                )
                deleted = True
        else:
            deleted = self.table.delete_item(Key={"uid": uid})
        return bool(deleted)

    def find_by_fieldname(self, name, value):
        """Get items selected by current field's name & value."""
        response = self.table.scan(
            FilterExpression=Attr(name).eq(value)
        )
        items = response.get("Items", [])
        return items

    def find_by_email(self, email):
        """Get all items selected by email field."""
        response = self.table.scan(
            FilterExpression=Attr("email").eq(email)
        )
        items = response.get("Items", [])
        return items
