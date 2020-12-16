import boto3
import codecs
import csv
from datetime import datetime
import json
import os

from constants import FILE_NAME
from utils import bad_request, response


WRITE_TO_BUCKET_NAME = os.environ.get("WRITE_TO_BUCKET_NAME")
s3 = boto3.client("s3")
delimiter = ";"


class Pipe:
    """Helper class for writing csv to a bucket."""
    value = ""

    def write(self, text):
        self.value = self.value + text


def handler(event, context):
    try:
        entry = json.loads(event["body"])["entry"]
    except Exception:
        return bad_request("There is no 'entry' in request body!")

    # read
    rows = list()
    try:
        obj = s3.get_object(Bucket=WRITE_TO_BUCKET_NAME, Key=FILE_NAME)
        body = csv.DictReader(codecs.getreader("utf-8")(obj["Body"]), delimiter=delimiter)
        for i, row in enumerate(body):  # add chunks in case of a big file?
            rows.append(dict(row))
    except (s3.exceptions.NoSuchKey, KeyError):
        pass
    except s3.exceptions.NoSuchBucket:
        return bad_request("No bucket with name " + WRITE_TO_BUCKET_NAME + "!")

    # add new
    next_id = 1 + max([int(row["id"]) for row in rows] or [0])
    date = datetime.now().strftime("%d.%m.%Y %H:%M")
    rows.append({
        "id": str(next_id),
        "created_at": date,
        "text": entry
    })

    # write
    pipe = Pipe()
    writer = csv.DictWriter(pipe, ["id", "created_at", "text"], delimiter=delimiter)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

    s3.put_object(Body=str.encode(pipe.value), Bucket=WRITE_TO_BUCKET_NAME, Key=FILE_NAME)

    return response(200, {"message": "New entry was added",
                          "last_records": rows[-10:]})
