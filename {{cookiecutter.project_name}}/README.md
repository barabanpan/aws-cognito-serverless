# Create API using AWS API Gateway, Lambda, Cognito, DynamoDB and Serverless

In one button press creates a small project with 
 - sign up, 
 - sign in, 
 - a resource for unregistered users, 
 - a protected resource (only accessible with an access token),
 - URL for writing entries to s3 bucket file.

For CRUD operations:
 - get all (entities/) and get by uid (entities/{uid}),
 - post a new entity (entities/),
 - delete by uid (entities/{uid}).

**TODO**: add s3 bucket with Swagger documentation.

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
3. Go here ([AWS SES configuration](https://eu-west-1.console.aws.amazon.com/ses/home?region=eu-west-1#verified-senders-email:)) to create and verify an email address.

Replace `From` and `SourceArn` with your email address and its arn in `serverless.yaml` file (Resources.CognitoUserPool.Properties.EmailConfiguration)

It's needed for sending verification emails and usually email looks like *no-reply@ourcompanyname.com*.
For tests you can use your own email.
You only need one email for all stages. 

4. Run with:
```
sls deploy --stage dev
```
or whatever stage name you want.
Running the command again with a different name will create a seperate API.

5. Use Postman collection to test API.
For sign up better use a real email to receive a verification message.
