# format for Entity date field
DATE_FORMAT = "%Y-%m-%d"

DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S %Z"

# file name in bucket for writing
FILE_NAME = "{{cookiecutter.s3_file_name}}.txt"

# list of available cognito groups for users
COGNITO_USER_POOL_GROUPS = ["reader", "modifier"]
