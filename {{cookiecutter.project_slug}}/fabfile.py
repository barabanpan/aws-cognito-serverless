"""
Please install fabric3 before run command from this module.
Install fabric3 from console:
>>> python3 -m pip install -U pip
>>> python3 -m pip install -U fabric3
"""


from fabric.api import local, task


@task
def sls_install():
    """Install serverless requirements."""
    local("npm install -g serverless")
    local("sls plugin install -n serverless-iam-roles-per-function")
    local("sls plugin install -n serverless-s3-sync")
    local("sls plugin install -n serverless-python-requirements")


@task
def sls_deploy(stage="dev"):
    """Deploy project on AWS with Serverless framework."""
    local(f"sls deploy --stage {stage}")
