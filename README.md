# Template for API using AWS API Gateway, Lambda, Cognito, DynamoDB and Serverless

Create a project with 
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

**TODO**: add s3 bucket with Swagger documentation.

## How To Run It

1. Install python and pip

2. Install cookiecutter:
```
pip istall cookiecutter
```

3. Go here ([AWS SES configuration](https://eu-west-1.console.aws.amazon.com/ses/home?region=eu-west-1#verified-senders-email:)) to create and verify an email address.

Note your SES region and your email, you'll need them in step 4.

It's needed for sending verification emails and usually email looks like *no-reply@ourcompanyname.com*.
For tests you can use your own email.
You only need one email for all stages. 


4. Create project from template (in a folder, seperate from template):
```
cookiecutter https://github.com/barabanpan/aws-cognito-serverless.git
```

Choose parameters. Better write entity_name in plural from. No pressure though:)
> project_name should match the next pattern "[a-zA-Z][0-9a-zA-Z-]+$"

5. For further steps see README.md inside of {{cookiecutter.project_name}} folder.
