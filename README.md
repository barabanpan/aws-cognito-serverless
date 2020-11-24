# Create API using AWS API Gateway, Lambda, Cognito, DynamoDB and Serverless

In one button press creates a small project with 
 - sign up, 
 - sign in, 
 - a resource for unregistered users, 
 - a protected resource (only accessible with an access token).
For CRUD operations:
 - get all (entities/) and get by username (entities/{username}),
 - post a new entity (entities/),
 - delete by username (entities/{username}).

**TODO**: validation with Marshmallow, s3 interaction, add CookieCutter.

## How To Run It

1. Install Serverless

2. Set your AWS credentials:

```export AWS_ACCESS_KEY_ID=<your_key_id_here>```

```export AWS_SECRET_ACCESS_KEY=<your_secret_key_here>```

For Windows use `set` instead of `export`.

3. Go here ([AWS SES configuration](https://eu-west-1.console.aws.amazon.com/ses/home?region=eu-west-1#verified-senders-email:)) to create and verify an email address.
Replace `From` and `SourceArn` with your email address and its arn in `serverless.yaml` file (Resources.CognitoUserPool.Properties.EmailConfiguration)

It's needed for sending verification emails and usually email looks like *no-reply@ourcompanyname.com*.
For tests you can use your own email.
You only need one email for all stages. 

4. Run with:

```sls deploy --stage dev```

or whatever stage name you want.
Running the command again with a different name will create a seperate API.

5. Use Postman collection to test API.
For sign up better use a real email to receive a verification message.
