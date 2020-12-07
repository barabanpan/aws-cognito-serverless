# {{cookiecutter.project_name }}


In one button press creates a small project with 
 - sign up, 
 - sign in, 
 - a resource for unregistered users, 
 - a protected resource (only accessible with an access token),
 - URL for writing entries to s3 bucket file.

For CRUD operations:
 - get all (entities/) and get by uid (entities/{uid}),
 - post a new entity (entities/),
 - put by uid (entities/{uid}),
 - delete by uid (entities/{uid}).

**TODO**: add Cognito groups or RBAC.

## How To Run It
1. Install node.js LTS version & dependencies:

1.1. Install or check npm (npm -v) 

1.2. Install Serverless:

```
npm install -g serverless
```

  > If there is an error with "node<10.00", first run:
  > `apt-get install nodejs:i386`

1.3. Install serverless plugins:

```
sls plugin install -n serverless-s3-sync
sls plugin install -n serverless-python-requirements
```

2. Set your AWS credentials:
```
export AWS_ACCESS_KEY_ID=<your_key_id_here>
```
```
export AWS_SECRET_ACCESS_KEY=<your_secret_key_here>
```

3. Run with:
```
sls deploy --stage dev
```
or whatever stage name you want.
Running the command again with a different name will create a seperate API.

4. Copy your API URL from cmd. It'll look like this https://ab12cd34e5.execute-api.eu-central-1.amazonaws.com/dev and insert it into swagger_s3_bucket/docs.yaml in servers.url
To deploy changes, run again: 
```
sls deploy --stage dev
```

5. Use Postman collection to test API.
For sign up better use a real email to receive a verification message.


Licence: {{cookiecutter.license }}
