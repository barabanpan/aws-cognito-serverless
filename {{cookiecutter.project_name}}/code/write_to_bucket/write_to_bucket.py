import boto3
from datetime import datetime
import json
import os

from constants import FILE_NAME
from utils import bad_request, response


WRITE_TO_BUCKET_NAME = os.environ.get("WRITE_TO_BUCKET_NAME")
s3 = boto3.client("s3")


def handler(event, context):
    try:
        entry = json.loads(event["body"])["entry"]
    except Exception as e:
        return bad_request("There is no entry in request body!")

    try:
        obj = s3.get_object(Bucket=WRITE_TO_BUCKET_NAME, Key=FILE_NAME)
        body = obj["Body"].read().decode("utf-8") + "\n\n"  # add chunks in case of a big file?
    except (s3.exceptions.NoSuchKey, KeyError):
        body = ""
    except s3.exceptions.NoSuchBucket:
        return bad_request("No bucket with name " + WRITE_TO_BUCKET_NAME + "!")

    date = datetime.now().strftime("%d.%m.%Y %H:%M")
    body += date + "\n" + entry

    s3.put_object(Body=str.encode(body), Bucket=WRITE_TO_BUCKET_NAME, Key=FILE_NAME)

    return response(200, {"message": "New entry was added"})
