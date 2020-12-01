import boto3
import time
import os


USERS_TABLE_NAME = os.environ.get("USERS_TABLE_NAME")
ENTITY_TABLE_NAME = os.environ.get("CRUD_ENTITY_TABLE_NAME")


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
        self.table.put_item(
            Item={
                "username": entity.username,  # key
                "email": entity.email,
                "description": entity.description,
                "value": entity.value,
                "date": entity.date,
                "is_good_boy": entity.is_good_boy
            }
        )

    def get_entity(self, username):
        entity = self.table.get_item(Key={"username": username}).get("Item")
        if not entity:
            return None
        return self.__prettify_response(entity)

    def get_all(self):
        all_entities = self.table.scan()["Items"]
        return [self.__prettify_response(response) for response in all_entities]

    def update_entity(self, entity):
        self.table.update_item(
            Key={"username": entity.username},  # чи можна міняти ключ??
            UpdateExpression="set username=:u, email=:e, description=:d, value=:v, date=:t, is_good_boy=:b",
            ExpressionAttributeValues={
                ":u": entity.username,
                ":e": entity.email,
                ":d": entity.description,
                ":v": entity.value,
                ":t": entity.date,
                ":b": entity.is_good_boy
            }
        )

    def delete_entity(self, username):
        self.table.delete_item(Key={"username": username})

    def __prettify_response(self, response):
        return {
            "username": response["username"],
            "email": response["email"],
            "description": response["description"],
            "value": int(response["value"]),
            "date": response["date"],
            "is_good_boy": response["is_good_boy"]
        }
