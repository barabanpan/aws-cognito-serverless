import boto3
import time
import os
import uuid


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

    def add_new_entity(self, entity):
        uid = str(uuid.uuid4())
        self.table.put_item(
            Item={
                "uid": uid,  # key
                "email": entity.email,
                "description": entity.description,
                "value": entity.value,
                "date": entity.date,
                "is_good_boy": entity.is_good_boy
            }
        )
        return uid

    def get_entity(self, uid):
        entity = self.table.get_item(Key={"uid": uid}).get("Item")
        if not entity:
            return None
        return self.__prettify_response(entity)

    def get_all(self):
        all_entities = self.table.scan()["Items"]
        return [self.__prettify_response(response) for response in all_entities]

    def delete_entity(self, uid):
        self.table.delete_item(Key={"uid": uid})

    def __prettify_response(self, response):
        return {
            "uid": response["uid"],
            "email": response["email"],
            "description": response["description"],
            "value": int(response["value"]),
            "date": response["date"],
            "is_good_boy": response["is_good_boy"]
        }
