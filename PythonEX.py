# Python script that autheticates with AWS via the sts client with boto3
# and then uses the credentials to list the buckets in the account

import boto3
import json

# Create the sts client. Credentials will be pulled from enviroment variables or AWS credentials.
sts_client = boto3.client('sts')

# Call the assume_role method of the STSConnection object and pass the role
# ARN and a role session name.
assumedRoleObject = sts_client.assume_role(
    RoleArn="arn:aws:iam::123456789012:role/role-name",
    RoleSessionName="AssumeRoleSession1" )

# From the response that contains the assumed role, get the temporary
# credentials that can be used to make subsequent API calls
credentials = assumedRoleObject['Credentials']

# Function that creates a S3 bucket
def create_bucket(bucket_name, region=None):
    try:
        s3_client = boto3.client('s3')
        s3_client.create_bucket(Bucket=bucket_name)
    except Exception as e:
        print(e)
        return False
    return True 

    # Function that creates and applies S3 bucket policy with upload and download permissions
def create_bucket_policy(bucket_name):
    try:
        s3_client = boto3.client('s3')
        bucket_policy = {
            'Version': '2012-10-17',
            'Statement': [{
                'Sid': 'AddPerm',
                'Effect': 'Allow',
                'Principal': '*',
                'Action': ['s3:GetObject'],
                'Resource': "arn:aws:s3:::%s/*" % bucket_name
            }]
        }
        bucket_policy = json.dumps(bucket_policy)
        s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
    except Exception as e:
        print(e)
        return False
    return True
    
