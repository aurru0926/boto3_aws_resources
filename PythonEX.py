## This is Python script that autheticates with AWS through the sts client with boto3
## and then uses the credentials to list the buckets in the account.

import boto3
import json

sts_client = boto3.client('sts')

assumedRoleObject = sts_client.assume_role(
    RoleArn="arn:aws:iam::123456789012:role/role-name",
    RoleSessionName="AssumeRoleSession1" )

credentials = assumedRoleObject['Credentials']

## This Function creates a S3 bucket
def create_bucket(bucket_name, region=None):
    try:
        s3_client = boto3.client('s3')
        s3_client.create_bucket(Bucket=bucket_name)
    except Exception as e:
        print(e)
        return False
    return True 

    ## This function creates and applies S3 bucket policy.
def create_bucket_policy(bucket_name):
    try:
        s3_client = boto3.client('s3')
        bucket_policy = {
            'Version': '2012-10-17',
            'Statement': [{
                'Sid': 'AddPerm',
                'Effect': 'Allow',
                'Principal': {'Service': 'lambda.amazonaws.com'},
                'Action': ['s3:GetObject','s3:PutObject'],
                'Resource': "arn:aws:s3:::%s/*" % bucket_name
            }]
        }
        bucket_policy = json.dumps(bucket_policy)
        s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
    except Exception as e:
        print(e)
        return False
    return True
    
    ## This creates an EC2 instance.
   def create_ec2_instance():
    try:
        ec2 = boto3.resource('ec2')
        instance = ec2.create_instances(
            ImageId='ami-0b898040803850657',
            MinCount=1,
            MaxCount=4,
            InstanceType='t2.micro',
            KeyName='my-key-pair'
        )
    except Exception as e:
        print(e)
        return False
    return True

    ## This creates an IAM role and is attached to the EC2 instance.
def create_iam_role(role_name):
    try:
        iam = boto3.client('iam')
        role = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(
                {'Statement': [{'Action': 'sts:AssumeRole',
                                'Effect': 'Allow',
                                'Principal': {'Service': 'ec2.amazonaws.com'}}],
                 'Version': '2012-10-17'})
        )
    except Exception as e:
        print(e)
        return False
    return True

def attach_policy(role_name):
    try:
        iam = boto3.client('iam')
        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess'
        )
    except Exception as e:
        print(e)
        return False
    return True

   ## This creates a lambda function with its respective IAM role.
def create_iam_role_lambda(role_name, function_name):
    try:
        iam = boto3.client('iam')
        role = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(
                {'Statement': [{'Action': 'sts:AssumeRole',
                                'Effect': 'Allow',
                                'Principal': {'Service': 'lambda.amazonaws.com'}}],
                 'Version': '2012-10-17'})
        )
        lambda_client = boto3.client('lambda')
        lambda_client.update_function_configuration(
            FunctionName=function_name,
            Role=role['Role']['Arn']
        )
    except Exception as e:
        print(e)
        return False
    return True

## Here we create a function to invoke lambda.
def create_policy_for_lambda(function_name):
    try:
        lambda_client = boto3.client('lambda')
        lambda_client.add_permission(
            FunctionName=function_name,
            StatementId='lambda',
            Action='lambda:InvokeFunction',
            Principal='s3.amazonaws.com',
            SourceArn='arn:aws:s3:::my-bucket'
        )
    except Exception as e:
        print(e)
        return False
    return True
