# Create API using AWS API Gateway, Lambda, Cognito, DynamoDB and Serverless

Create a project that in one button press creates a small project with 
 - sign up, 
 - sign in, 
 - a resource for unregistered users, 
 - a protected resource (only accessible with an access token),
 - URL for writing entries to s3 bucket file.

For CRUD operations:
 - get all (entities/) and get by username (entities/{username}),
 - post a new entity (entities/),
 - delete by username (entities/{username}).

**TODO**: add s3 bucket with Swagger documentation. Add CookieCutter.

## How To Run It

1. Install python and pip

2. Install cookiecutter:
```
pip istall cookiecutter
```

3. Create project from template (in a folder, seperate from template):
```
cookiecutter <path_to_template_here>
```

Choose parameters. Better write entity_name in plural from. No pressure though:)

4. For further steps see REAME.md inside of {{cookiecutter.project_name}} folder.
