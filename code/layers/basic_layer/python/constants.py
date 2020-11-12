import os


# cognito app client credentials
CLIENT_ID = os.environ.get('COGNITO_CLIENT_ID')  # do it here or pass some other way?
CLIENT_SECRET = os.environ.get('COGNITO_CLIENT_SECRET')

# table with users' information
USERS_TABLE_NAME = os.environ.get('USERS_TABLE_NAME')
